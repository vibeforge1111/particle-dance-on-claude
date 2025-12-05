"""
Particle system with soft-body fluid dynamics.
"""
import numpy as np
import math
import random


class ParticleSystem:
    """Manages all particles with vectorized physics calculations."""

    def __init__(self, max_particles=1500, width=1920, height=1080):
        self.max_particles = max_particles
        self.width = width
        self.height = height

        # Physics parameters from PRD
        self.gravity = 0.02
        self.buoyancy = 0.015
        self.viscosity = 0.95
        self.collision_softness = 0.3

        # Particle arrays (vectorized for performance)
        self.count = 0
        self.positions = np.zeros((max_particles, 2), dtype=np.float32)
        self.velocities = np.zeros((max_particles, 2), dtype=np.float32)
        self.accelerations = np.zeros((max_particles, 2), dtype=np.float32)
        self.colors = np.zeros((max_particles, 3), dtype=np.float32)  # HSV
        self.sizes = np.zeros(max_particles, dtype=np.float32)
        self.masses = np.zeros(max_particles, dtype=np.float32)
        self.temperatures = np.zeros(max_particles, dtype=np.float32)  # For buoyancy
        self.lifetimes = np.zeros(max_particles, dtype=np.float32)
        self.trail_alpha = np.zeros(max_particles, dtype=np.float32)

        # Color palette from PRD (HSV values)
        self.color_palette = [
            (330, 1.0, 1.0),   # Magenta #FF006E
            (190, 1.0, 0.83),  # Cyan #00D4FF
            (43, 1.0, 1.0),    # Amber #FFB800
            (265, 0.77, 0.93), # Violet #8338EC
            (158, 0.97, 1.0),  # Mint #06FFA5
        ]

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

        if size is None:
            self.sizes[i] = random.uniform(4, 12)
        else:
            self.sizes[i] = size

        self.masses[i] = self.sizes[i] * 0.1
        self.temperatures[i] = random.uniform(0.3, 1.0)
        self.lifetimes[i] = 1.0
        self.trail_alpha[i] = 1.0

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

    def apply_force(self, center_x, center_y, radius, strength, repel=False):
        """Apply attract/repel force from a point."""
        if self.count == 0:
            return 0

        # Vectorized distance calculation
        active_pos = self.positions[:self.count]
        dx = active_pos[:, 0] - center_x
        dy = active_pos[:, 1] - center_y
        distances = np.sqrt(dx * dx + dy * dy)

        # Only affect particles within radius
        mask = distances < radius
        affected_count = np.sum(mask)

        if affected_count == 0:
            return 0

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

        return affected_count

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

    def explode_from_point(self, center_x, center_y, radius, strength):
        """Explosive scatter from a point."""
        return self.apply_force(center_x, center_y, radius, strength, repel=True)

    def update(self, dt=1.0):
        """Update particle physics."""
        if self.count == 0:
            return

        active = slice(0, self.count)

        # Apply gravity
        self.accelerations[active, 1] = self.gravity

        # Apply buoyancy (warm particles rise)
        buoyancy_force = -self.buoyancy * self.temperatures[active]
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
            return [], [], [], []

        active = slice(0, self.count)
        return (
            self.positions[active].copy(),
            self.colors[active].copy(),
            self.sizes[active].copy(),
            self.trail_alpha[active].copy()
        )

    def resize(self, width, height):
        """Handle window resize."""
        # Scale particle positions proportionally
        if self.count > 0:
            self.positions[:self.count, 0] *= width / self.width
            self.positions[:self.count, 1] *= height / self.height

        self.width = width
        self.height = height
