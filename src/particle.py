"""
Particle system with soft-body fluid dynamics, merging, and bubble formation.
"""
import numpy as np
import math
import random
from quadtree import SpatialHash


class ParticleSystem:
    """Manages all particles with vectorized physics calculations."""

    def __init__(self, max_particles=1500, width=1920, height=1080):
        self.max_particles = max_particles
        self.width = width
        self.height = height

        # Physics parameters from PRD
        self.gravity = 0.02
        self.gravity_direction = 1  # 1 = down, -1 = up
        self.buoyancy = 0.015
        self.viscosity = 0.95
        self.collision_softness = 0.3

        # Merging parameters
        self.merge_distance = 15  # Distance at which particles start merging
        self.merge_rate = 0.02    # How fast particles merge
        self.max_particle_size = 40  # Maximum blob size
        self.bubble_threshold = 25  # Size at which particle becomes a "bubble"

        # Color transition
        self.color_shift_speed = 0.1  # How fast colors shift

        # Particle arrays (vectorized for performance)
        self.count = 0
        self.positions = np.zeros((max_particles, 2), dtype=np.float32)
        self.velocities = np.zeros((max_particles, 2), dtype=np.float32)
        self.accelerations = np.zeros((max_particles, 2), dtype=np.float32)
        self.colors = np.zeros((max_particles, 3), dtype=np.float32)  # HSV
        self.target_colors = np.zeros((max_particles, 3), dtype=np.float32)  # For transitions
        self.sizes = np.zeros(max_particles, dtype=np.float32)
        self.masses = np.zeros(max_particles, dtype=np.float32)
        self.temperatures = np.zeros(max_particles, dtype=np.float32)  # For buoyancy
        self.lifetimes = np.zeros(max_particles, dtype=np.float32)
        self.trail_alpha = np.zeros(max_particles, dtype=np.float32)
        self.is_bubble = np.zeros(max_particles, dtype=bool)  # Bubble state

        # Color palettes from PRD (HSV values)
        self.color_palettes = {
            'default': [
                (330, 1.0, 1.0),   # Magenta #FF006E
                (190, 1.0, 0.83),  # Cyan #00D4FF
                (43, 1.0, 1.0),    # Amber #FFB800
                (265, 0.77, 0.93), # Violet #8338EC
                (158, 0.97, 1.0),  # Mint #06FFA5
            ],
            'sunset': [
                (15, 1.0, 1.0),    # Orange-red
                (35, 1.0, 1.0),    # Orange
                (50, 0.9, 1.0),    # Golden
                (340, 0.8, 0.9),   # Pink
                (280, 0.6, 0.8),   # Lavender
            ],
            'ocean': [
                (200, 1.0, 0.9),   # Deep blue
                (180, 0.8, 1.0),   # Cyan
                (160, 0.9, 0.8),   # Teal
                (220, 0.7, 0.6),   # Navy
                (190, 0.5, 1.0),   # Light blue
            ],
            'aurora': [
                (120, 1.0, 0.9),   # Green
                (160, 0.9, 1.0),   # Cyan-green
                (280, 0.8, 0.9),   # Purple
                (200, 0.7, 1.0),   # Blue
                (80, 0.6, 1.0),    # Yellow-green
            ],
            'monochrome': [
                (0, 0.0, 1.0),     # White
                (0, 0.0, 0.8),     # Light gray
                (0, 0.0, 0.6),     # Medium gray
                (0, 0.0, 0.9),     # Near white
                (0, 0.0, 0.7),     # Gray
            ],
        }
        self.current_palette = 'default'
        self.color_palette = self.color_palettes['default']

        # Merging events for audio feedback
        self.recent_merges = 0

        # Screensaver/idle mode
        self.idle_mode = False
        self.idle_time = 0
        self.idle_flow_angle = 0
        self.idle_flow_centers = []  # Random attractor points

        # Spatial partitioning for efficient queries
        self.spatial_hash = SpatialHash(width, height, cell_size=50)

        # Initialize with starting particles
        self.spawn_initial_particles(500)

    def spawn_initial_particles(self, count):
        """Spawn initial particles distributed across screen."""
        for _ in range(count):
            x = random.uniform(100, self.width - 100)
            y = random.uniform(100, self.height - 100)
            self.spawn_particle(x, y)

    def spawn_particle(self, x, y, velocity=None, color=None, size=None):
        """Spawn a single particle at position."""
        if self.count >= self.max_particles:
            return False

        i = self.count
        self.positions[i] = [x, y]

        if velocity is None:
            # Random gentle drift
            self.velocities[i] = [
                random.uniform(-0.5, 0.5),
                random.uniform(-0.5, 0.5)
            ]
        else:
            self.velocities[i] = velocity

        self.accelerations[i] = [0, 0]

        if color is None:
            # Pick from palette with slight variation
            base_color = random.choice(self.color_palette)
            self.colors[i] = [
                (base_color[0] + random.uniform(-15, 15)) % 360,
                base_color[1] * random.uniform(0.8, 1.0),
                base_color[2] * random.uniform(0.8, 1.0)
            ]
        else:
            self.colors[i] = color

        # Set target color for smooth transition
        next_color = random.choice(self.color_palette)
        self.target_colors[i] = [
            (next_color[0] + random.uniform(-15, 15)) % 360,
            next_color[1] * random.uniform(0.8, 1.0),
            next_color[2] * random.uniform(0.8, 1.0)
        ]

        if size is None:
            self.sizes[i] = random.uniform(4, 12)
        else:
            self.sizes[i] = size

        self.masses[i] = self.sizes[i] * 0.1
        self.temperatures[i] = random.uniform(0.3, 1.0)
        self.lifetimes[i] = 1.0
        self.trail_alpha[i] = 1.0
        self.is_bubble[i] = False

        self.count += 1
        return True

    def spawn_cluster(self, x, y, count=20, spread=30):
        """Spawn a cluster of particles."""
        spawned = 0
        for _ in range(count):
            px = x + random.gauss(0, spread)
            py = y + random.gauss(0, spread)
            vel = [random.uniform(-1, 1), random.uniform(-1, 1)]
            if self.spawn_particle(px, py, velocity=vel):
                spawned += 1
        return spawned

    def set_gravity_direction(self, direction):
        """Set gravity direction: 1 = down, -1 = up, 0 = none."""
        self.gravity_direction = direction

    def apply_force(self, center_x, center_y, radius, strength, repel=False):
        """Apply attract/repel force from a point. Returns (affected_count, touching_count)."""
        if self.count == 0:
            return 0, 0

        # Vectorized distance calculation
        active_pos = self.positions[:self.count]
        dx = active_pos[:, 0] - center_x
        dy = active_pos[:, 1] - center_y
        distances = np.sqrt(dx * dx + dy * dy)

        # Only affect particles within radius
        mask = distances < radius
        affected_count = np.sum(mask)

        # Count particles very close (touching hand hitbox)
        touch_radius = 50
        touching_mask = distances < touch_radius
        touching_count = np.sum(touching_mask)

        if affected_count == 0:
            return 0, touching_count

        # Calculate force magnitude (inverse square falloff)
        safe_distances = np.maximum(distances[mask], 1.0)
        force_mag = strength / (safe_distances * 0.1 + 1)

        # Normalize direction
        nx = dx[mask] / safe_distances
        ny = dy[mask] / safe_distances

        # Apply force (repel or attract)
        if repel:
            self.velocities[:self.count, 0][mask] += nx * force_mag
            self.velocities[:self.count, 1][mask] += ny * force_mag
        else:
            self.velocities[:self.count, 0][mask] -= nx * force_mag
            self.velocities[:self.count, 1][mask] -= ny * force_mag

        # Heat up particles when touched
        self.temperatures[:self.count][touching_mask] = np.minimum(
            self.temperatures[:self.count][touching_mask] + 0.1, 1.0
        )

        return affected_count, touching_count

    def apply_vortex(self, center_x, center_y, radius, strength):
        """Apply swirling vortex force."""
        if self.count == 0:
            return 0

        active_pos = self.positions[:self.count]
        dx = active_pos[:, 0] - center_x
        dy = active_pos[:, 1] - center_y
        distances = np.sqrt(dx * dx + dy * dy)

        mask = distances < radius
        affected_count = np.sum(mask)

        if affected_count == 0:
            return 0

        safe_distances = np.maximum(distances[mask], 1.0)
        force_mag = strength * (1 - distances[mask] / radius)

        # Perpendicular force for rotation
        nx = -dy[mask] / safe_distances
        ny = dx[mask] / safe_distances

        self.velocities[:self.count, 0][mask] += nx * force_mag
        self.velocities[:self.count, 1][mask] += ny * force_mag

        return affected_count

    def apply_directional_flow(self, direction_x, direction_y, strength):
        """Apply directional flow (wave gesture)."""
        if self.count == 0:
            return

        # Normalize direction
        mag = math.sqrt(direction_x * direction_x + direction_y * direction_y)
        if mag > 0:
            direction_x /= mag
            direction_y /= mag

        self.velocities[:self.count, 0] += direction_x * strength
        self.velocities[:self.count, 1] += direction_y * strength

    def attract_between_points(self, x1, y1, x2, y2, radius, strength):
        """Attract particles in a region between two points (two hands merge)."""
        if self.count == 0:
            return 0

        # Center point between hands
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        active_pos = self.positions[:self.count]
        dx = active_pos[:, 0] - cx
        dy = active_pos[:, 1] - cy
        distances = np.sqrt(dx * dx + dy * dy)

        # Affect particles near the center
        mask = distances < radius
        affected_count = np.sum(mask)

        if affected_count == 0:
            return 0

        safe_distances = np.maximum(distances[mask], 1.0)
        force_mag = strength / (safe_distances * 0.05 + 1)

        # Pull toward center
        nx = dx[mask] / safe_distances
        ny = dy[mask] / safe_distances

        self.velocities[:self.count, 0][mask] -= nx * force_mag
        self.velocities[:self.count, 1][mask] -= ny * force_mag

        # Heat up particles being merged
        self.temperatures[:self.count][mask] = np.minimum(
            self.temperatures[:self.count][mask] + 0.05, 1.0
        )

        return affected_count

    def explode_from_point(self, center_x, center_y, radius, strength):
        """Explosive scatter from a point."""
        affected, _ = self.apply_force(center_x, center_y, radius, strength, repel=True)
        return affected

    def _process_merging(self):
        """Process particle merging - nearby particles combine into larger blobs."""
        if self.count < 2:
            return

        self.recent_merges = 0
        particles_to_remove = set()

        # Build spatial hash for current frame
        self.spatial_hash.clear()
        for i in range(self.count):
            self.spatial_hash.insert(i, self.positions[i, 0], self.positions[i, 1])

        # Check a random subset of particles each frame
        check_count = min(self.count, 150)
        indices = random.sample(range(self.count), check_count)

        for i in indices:
            if i in particles_to_remove:
                continue

            # Use spatial hash to find nearby particles (much faster than O(n²))
            merge_radius = self.max_particle_size * 1.5
            nearby = self.spatial_hash.query_radius(
                self.positions[i, 0],
                self.positions[i, 1],
                merge_radius
            )

            for j, px, py, dist in nearby:
                if j <= i or j in particles_to_remove:
                    continue

                merge_threshold = (self.sizes[i] + self.sizes[j]) * 0.5

                if dist < merge_threshold:
                    # Merge j into i
                    total_mass = self.masses[i] + self.masses[j]

                    # Weighted average position
                    self.positions[i] = (
                        self.positions[i] * self.masses[i] +
                        self.positions[j] * self.masses[j]
                    ) / total_mass

                    # Weighted average velocity
                    self.velocities[i] = (
                        self.velocities[i] * self.masses[i] +
                        self.velocities[j] * self.masses[j]
                    ) / total_mass

                    # Blend colors
                    self.colors[i] = (self.colors[i] + self.colors[j]) / 2

                    # Grow size (with limit)
                    new_size = min(
                        self.sizes[i] + self.sizes[j] * 0.3,
                        self.max_particle_size
                    )
                    self.sizes[i] = new_size
                    self.masses[i] = new_size * 0.1

                    # Check if it's now a bubble
                    if new_size >= self.bubble_threshold:
                        self.is_bubble[i] = True
                        self.temperatures[i] = min(self.temperatures[i] + 0.2, 1.0)

                    particles_to_remove.add(j)
                    self.recent_merges += 1
                    break  # Only one merge per particle per frame

        # Remove merged particles
        if particles_to_remove:
            self._remove_particles(particles_to_remove)

    def _remove_particles(self, indices_to_remove):
        """Remove particles by indices."""
        indices = sorted(indices_to_remove, reverse=True)
        for idx in indices:
            if idx < self.count - 1:
                # Swap with last particle
                self.positions[idx] = self.positions[self.count - 1]
                self.velocities[idx] = self.velocities[self.count - 1]
                self.accelerations[idx] = self.accelerations[self.count - 1]
                self.colors[idx] = self.colors[self.count - 1]
                self.target_colors[idx] = self.target_colors[self.count - 1]
                self.sizes[idx] = self.sizes[self.count - 1]
                self.masses[idx] = self.masses[self.count - 1]
                self.temperatures[idx] = self.temperatures[self.count - 1]
                self.lifetimes[idx] = self.lifetimes[self.count - 1]
                self.trail_alpha[idx] = self.trail_alpha[self.count - 1]
                self.is_bubble[idx] = self.is_bubble[self.count - 1]
            self.count -= 1

    def _update_colors(self):
        """Smoothly transition colors (lava lamp effect)."""
        if self.count == 0:
            return

        active = slice(0, self.count)

        # Interpolate toward target colors
        color_diff = self.target_colors[active] - self.colors[active]

        # Handle hue wrapping
        hue_diff = color_diff[:, 0]
        hue_diff = np.where(hue_diff > 180, hue_diff - 360, hue_diff)
        hue_diff = np.where(hue_diff < -180, hue_diff + 360, hue_diff)
        color_diff[:, 0] = hue_diff

        self.colors[active] += color_diff * self.color_shift_speed * 0.01

        # Wrap hue
        self.colors[active, 0] = self.colors[active, 0] % 360

        # Check if we've reached target, set new target
        distances = np.abs(color_diff[:, 0])
        reached_target = distances < 5

        for i in np.where(reached_target)[0]:
            if i < self.count:
                next_color = random.choice(self.color_palette)
                self.target_colors[i] = [
                    (next_color[0] + random.uniform(-20, 20)) % 360,
                    next_color[1] * random.uniform(0.8, 1.0),
                    next_color[2] * random.uniform(0.8, 1.0)
                ]

    def _process_bubbles(self):
        """Process bubble behavior - large particles float up more."""
        if self.count == 0:
            return

        active = slice(0, self.count)
        bubble_mask = self.is_bubble[active]

        if not np.any(bubble_mask):
            return

        # Bubbles have extra buoyancy
        bubble_indices = np.where(bubble_mask)[0]
        self.velocities[bubble_indices, 1] -= 0.03 * self.gravity_direction

        # Bubbles slowly shrink (split off small particles)
        self.sizes[bubble_indices] -= 0.01
        small_bubbles = self.sizes[bubble_indices] < self.bubble_threshold
        self.is_bubble[bubble_indices[small_bubbles]] = False

        # Occasionally spawn small particles from bubbles
        if random.random() < 0.02 and len(bubble_indices) > 0:
            idx = random.choice(bubble_indices)
            if self.sizes[idx] > 15:
                x, y = self.positions[idx]
                self.spawn_particle(
                    x + random.uniform(-10, 10),
                    y + random.uniform(-10, 10),
                    velocity=[random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)],
                    size=random.uniform(3, 6)
                )
                self.sizes[idx] -= 2

    def update(self, dt=1.0):
        """Update particle physics."""
        if self.count == 0:
            return

        active = slice(0, self.count)

        # Apply gravity (with direction)
        self.accelerations[active, 1] = self.gravity * self.gravity_direction

        # Apply buoyancy (warm particles rise)
        buoyancy_force = -self.buoyancy * self.temperatures[active] * self.gravity_direction
        self.accelerations[active, 1] += buoyancy_force

        # Update velocities with acceleration
        self.velocities[active] += self.accelerations[active] * dt

        # Apply viscosity (drag)
        self.velocities[active] *= self.viscosity

        # Update positions
        self.positions[active] += self.velocities[active] * dt

        # Boundary handling (soft bounce)
        self._handle_boundaries()

        # Reset accelerations
        self.accelerations[active] = 0

        # Slowly cool particles
        self.temperatures[active] *= 0.999
        self.temperatures[active] = np.maximum(self.temperatures[active], 0.2)

        # Update trail alpha based on velocity
        speeds = np.linalg.norm(self.velocities[active], axis=1)
        self.trail_alpha[active] = np.clip(speeds * 0.5, 0.3, 1.0)

        # Process merging (every few frames for performance)
        if random.random() < 0.3:
            self._process_merging()

        # Update colors (lava lamp transitions)
        self._update_colors()

        # Process bubble behavior
        self._process_bubbles()

    def _handle_boundaries(self):
        """Soft boundary collision."""
        active = slice(0, self.count)
        margin = 50
        bounce = 0.5

        # Left boundary
        mask = self.positions[active, 0] < margin
        self.positions[active, 0] = np.where(mask, margin, self.positions[active, 0])
        self.velocities[active, 0] = np.where(mask, abs(self.velocities[active, 0]) * bounce, self.velocities[active, 0])

        # Right boundary
        mask = self.positions[active, 0] > self.width - margin
        self.positions[active, 0] = np.where(mask, self.width - margin, self.positions[active, 0])
        self.velocities[active, 0] = np.where(mask, -abs(self.velocities[active, 0]) * bounce, self.velocities[active, 0])

        # Top boundary
        mask = self.positions[active, 1] < margin
        self.positions[active, 1] = np.where(mask, margin, self.positions[active, 1])
        self.velocities[active, 1] = np.where(mask, abs(self.velocities[active, 1]) * bounce, self.velocities[active, 1])

        # Bottom boundary
        mask = self.positions[active, 1] > self.height - margin
        self.positions[active, 1] = np.where(mask, self.height - margin, self.positions[active, 1])
        self.velocities[active, 1] = np.where(mask, -abs(self.velocities[active, 1]) * bounce, self.velocities[active, 1])

    def get_particle_data(self):
        """Get active particle data for rendering."""
        if self.count == 0:
            return [], [], [], [], []

        active = slice(0, self.count)
        return (
            self.positions[active].copy(),
            self.colors[active].copy(),
            self.sizes[active].copy(),
            self.trail_alpha[active].copy(),
            self.is_bubble[active].copy()
        )

    def get_merge_count(self):
        """Get recent merge count for audio feedback."""
        return self.recent_merges

    def resize(self, width, height):
        """Handle window resize."""
        # Scale particle positions proportionally
        if self.count > 0:
            self.positions[:self.count, 0] *= width / self.width
            self.positions[:self.count, 1] *= height / self.height

        self.width = width
        self.height = height

        # Resize spatial hash
        self.spatial_hash.resize(width, height)

    def set_palette(self, palette_name):
        """Set the color palette by name."""
        if palette_name in self.color_palettes:
            self.current_palette = palette_name
            self.color_palette = self.color_palettes[palette_name]
            # Update target colors for existing particles
            for i in range(self.count):
                next_color = random.choice(self.color_palette)
                self.target_colors[i] = [
                    (next_color[0] + random.uniform(-15, 15)) % 360,
                    next_color[1] * random.uniform(0.8, 1.0),
                    next_color[2] * random.uniform(0.8, 1.0)
                ]
            return True
        return False

    def get_palette_names(self):
        """Get list of available palette names."""
        return list(self.color_palettes.keys())

    def next_palette(self):
        """Cycle to the next color palette."""
        names = self.get_palette_names()
        current_idx = names.index(self.current_palette)
        next_idx = (current_idx + 1) % len(names)
        self.set_palette(names[next_idx])
        return names[next_idx]

    def set_idle_mode(self, enabled):
        """Enable or disable screensaver idle mode."""
        if enabled and not self.idle_mode:
            # Initialize idle mode with random attractor points
            self.idle_flow_centers = [
                (random.uniform(self.width * 0.2, self.width * 0.8),
                 random.uniform(self.height * 0.2, self.height * 0.8))
                for _ in range(3)
            ]
            self.idle_flow_angle = 0
        self.idle_mode = enabled

    def update_idle_mode(self, dt):
        """Update particles in idle/screensaver mode with gentle autonomous movement."""
        if self.count == 0:
            return

        self.idle_time += dt
        self.idle_flow_angle += 0.005 * dt

        # Slowly move attractor points
        for i in range(len(self.idle_flow_centers)):
            cx, cy = self.idle_flow_centers[i]
            # Gentle circular drift
            angle = self.idle_flow_angle + i * (2 * math.pi / 3)
            cx += math.cos(angle) * 0.5
            cy += math.sin(angle) * 0.3

            # Keep within bounds
            cx = max(self.width * 0.1, min(self.width * 0.9, cx))
            cy = max(self.height * 0.1, min(self.height * 0.9, cy))
            self.idle_flow_centers[i] = (cx, cy)

        # Apply gentle forces from attractor points
        active = slice(0, self.count)
        active_pos = self.positions[active]

        for cx, cy in self.idle_flow_centers:
            dx = active_pos[:, 0] - cx
            dy = active_pos[:, 1] - cy
            distances = np.sqrt(dx * dx + dy * dy)

            # Gentle attraction with orbital component
            mask = distances > 50  # Don't pull particles too close
            safe_dist = np.maximum(distances, 1.0)

            # Radial attraction (very gentle)
            force_mag = 0.02 / (safe_dist * 0.01 + 1)
            nx = dx / safe_dist
            ny = dy / safe_dist

            self.velocities[:self.count, 0][mask] -= nx[mask] * force_mag[mask]
            self.velocities[:self.count, 1][mask] -= ny[mask] * force_mag[mask]

            # Tangential swirl (creates orbital motion)
            swirl_mag = 0.015 / (safe_dist * 0.01 + 1)
            self.velocities[:self.count, 0][mask] += (-ny[mask]) * swirl_mag[mask]
            self.velocities[:self.count, 1][mask] += nx[mask] * swirl_mag[mask]

        # Occasionally shift attractor positions
        if random.random() < 0.001:
            idx = random.randint(0, len(self.idle_flow_centers) - 1)
            self.idle_flow_centers[idx] = (
                random.uniform(self.width * 0.2, self.width * 0.8),
                random.uniform(self.height * 0.2, self.height * 0.8)
            )
