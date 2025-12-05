"""
Quadtree spatial partitioning for efficient particle queries.
"""
import numpy as np


class Rectangle:
    """Axis-aligned bounding box."""

    def __init__(self, x, y, w, h):
        self.x = x  # center x
        self.y = y  # center y
        self.w = w  # half width
        self.h = h  # half height

    def contains(self, px, py):
        """Check if point is within this rectangle."""
        return (self.x - self.w <= px < self.x + self.w and
                self.y - self.h <= py < self.y + self.h)

    def intersects(self, other):
        """Check if this rectangle intersects another."""
        return not (other.x - other.w > self.x + self.w or
                    other.x + other.w < self.x - self.w or
                    other.y - other.h > self.y + self.h or
                    other.y + other.h < self.y - self.h)


class QuadTree:
    """Quadtree for spatial partitioning of particles."""

    CAPACITY = 8  # Max particles per node before subdividing
    MAX_DEPTH = 8  # Prevent infinite subdivision

    def __init__(self, boundary, depth=0):
        """
        Initialize quadtree node.

        Args:
            boundary: Rectangle defining this node's bounds
            depth: Current depth in tree (for limiting subdivision)
        """
        self.boundary = boundary
        self.depth = depth
        self.particles = []  # List of (index, x, y) tuples
        self.divided = False

        # Child quadrants (created on subdivision)
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None

    def clear(self):
        """Clear all particles from the tree."""
        self.particles = []
        self.divided = False
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None

    def subdivide(self):
        """Split this node into four children."""
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w / 2
        h = self.boundary.h / 2

        nw = Rectangle(x - w, y - h, w, h)
        ne = Rectangle(x + w, y - h, w, h)
        sw = Rectangle(x - w, y + h, w, h)
        se = Rectangle(x + w, y + h, w, h)

        self.northwest = QuadTree(nw, self.depth + 1)
        self.northeast = QuadTree(ne, self.depth + 1)
        self.southwest = QuadTree(sw, self.depth + 1)
        self.southeast = QuadTree(se, self.depth + 1)

        self.divided = True

        # Redistribute existing particles to children
        for particle in self.particles:
            self._insert_into_children(particle)
        self.particles = []

    def _insert_into_children(self, particle):
        """Insert particle into appropriate child node."""
        idx, px, py = particle

        if self.northwest.boundary.contains(px, py):
            self.northwest.insert(idx, px, py)
        elif self.northeast.boundary.contains(px, py):
            self.northeast.insert(idx, px, py)
        elif self.southwest.boundary.contains(px, py):
            self.southwest.insert(idx, px, py)
        elif self.southeast.boundary.contains(px, py):
            self.southeast.insert(idx, px, py)

    def insert(self, index, x, y):
        """
        Insert a particle into the quadtree.

        Args:
            index: Particle index in the main arrays
            x, y: Particle position

        Returns:
            True if inserted, False if out of bounds
        """
        # Ignore if outside boundary
        if not self.boundary.contains(x, y):
            return False

        # If not subdivided and have capacity, add here
        if not self.divided and len(self.particles) < self.CAPACITY:
            self.particles.append((index, x, y))
            return True

        # Need to subdivide (if not at max depth)
        if not self.divided:
            if self.depth < self.MAX_DEPTH:
                self.subdivide()
            else:
                # At max depth, just add to this node
                self.particles.append((index, x, y))
                return True

        # Insert into children
        self._insert_into_children((index, x, y))
        return True

    def query_range(self, range_rect, found=None):
        """
        Find all particles within a rectangular range.

        Args:
            range_rect: Rectangle to search within
            found: List to append results to (created if None)

        Returns:
            List of (index, x, y) tuples for particles in range
        """
        if found is None:
            found = []

        # Skip if range doesn't intersect this node
        if not self.boundary.intersects(range_rect):
            return found

        # Check particles in this node
        for particle in self.particles:
            idx, px, py = particle
            if range_rect.contains(px, py):
                found.append(particle)

        # Check children
        if self.divided:
            self.northwest.query_range(range_rect, found)
            self.northeast.query_range(range_rect, found)
            self.southwest.query_range(range_rect, found)
            self.southeast.query_range(range_rect, found)

        return found

    def query_radius(self, cx, cy, radius):
        """
        Find all particles within a circular radius.

        Args:
            cx, cy: Center of search circle
            radius: Search radius

        Returns:
            List of (index, x, y, distance) tuples for particles in range
        """
        # First query the bounding rectangle
        range_rect = Rectangle(cx, cy, radius, radius)
        candidates = self.query_range(range_rect)

        # Filter to actual circle
        found = []
        radius_sq = radius * radius
        for idx, px, py in candidates:
            dx = px - cx
            dy = py - cy
            dist_sq = dx * dx + dy * dy
            if dist_sq <= radius_sq:
                found.append((idx, px, py, dist_sq ** 0.5))

        return found

    def query_nearest(self, cx, cy, radius, exclude_idx=None):
        """
        Find particles near a point, optionally excluding one.

        Args:
            cx, cy: Search center
            radius: Search radius
            exclude_idx: Particle index to exclude (e.g., self)

        Returns:
            List of (index, x, y, distance) tuples sorted by distance
        """
        found = self.query_radius(cx, cy, radius)

        if exclude_idx is not None:
            found = [(i, x, y, d) for i, x, y, d in found if i != exclude_idx]

        # Sort by distance
        found.sort(key=lambda p: p[3])
        return found


class SpatialHash:
    """
    Alternative to quadtree: spatial hashing for uniform distribution.
    Often faster for particles that are relatively uniform.
    """

    def __init__(self, width, height, cell_size=50):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cols = max(1, int(width / cell_size) + 1)
        self.rows = max(1, int(height / cell_size) + 1)
        self.cells = {}

    def clear(self):
        """Clear all particles."""
        self.cells = {}

    def _get_cell(self, x, y):
        """Get cell coordinates for a position."""
        col = max(0, min(self.cols - 1, int(x / self.cell_size)))
        row = max(0, min(self.rows - 1, int(y / self.cell_size)))
        return (col, row)

    def insert(self, index, x, y):
        """Insert a particle."""
        cell = self._get_cell(x, y)
        if cell not in self.cells:
            self.cells[cell] = []
        self.cells[cell].append((index, x, y))

    def query_radius(self, cx, cy, radius):
        """Find particles within radius of point."""
        found = []
        radius_sq = radius * radius

        # Get range of cells to check
        min_col = max(0, int((cx - radius) / self.cell_size))
        max_col = min(self.cols - 1, int((cx + radius) / self.cell_size))
        min_row = max(0, int((cy - radius) / self.cell_size))
        max_row = min(self.rows - 1, int((cy + radius) / self.cell_size))

        for col in range(min_col, max_col + 1):
            for row in range(min_row, max_row + 1):
                cell = (col, row)
                if cell in self.cells:
                    for idx, px, py in self.cells[cell]:
                        dx = px - cx
                        dy = py - cy
                        dist_sq = dx * dx + dy * dy
                        if dist_sq <= radius_sq:
                            found.append((idx, px, py, dist_sq ** 0.5))

        return found

    def get_potential_collisions(self, index, x, y, radius):
        """Get particles that might collide with given particle."""
        return self.query_radius(x, y, radius)

    def resize(self, width, height):
        """Update dimensions."""
        self.width = width
        self.height = height
        self.cols = max(1, int(width / self.cell_size) + 1)
        self.rows = max(1, int(height / self.cell_size) + 1)
