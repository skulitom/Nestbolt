"""Compare integer translation windows with direct rectangle intersection on small grids."""
from random import Random
from joint import cover, windows


def rectangle(rng):
    x,y = rng.randrange(-3,7),rng.randrange(-3,7)
    return x,x+rng.randrange(1,5),y,y+rng.randrange(1,5)


def inside(intervals,x,y):
    return sum(l <= x < r and b <= y < t for l,r,b,t in intervals)


if __name__ == "__main__":
    rng = Random(20261120)
    placements = 0
    for _ in range(100):
        fixed = [rectangle(rng) for _ in range(6)]
        local = [rectangle(rng) for _ in range(3)]
        filled = cover(fixed)
        allowed = windows(filled,local,-4,8,-4,8)
        for x in range(-4,9):
            for y in range(-4,9):
                assert inside(filled,x,y) == int(inside(fixed,x,y)>0)
                overlap = any(l < z+x and r > a+x and b < w+y and t > c+y
                              for l,r,b,t in fixed for a,z,c,w in local)
                count = sum(l <= x <= r and b <= y <= t for l,r,b,t in allowed)
                assert count == int(not overlap)
                placements += 1
    print(f"{placements} placements agreed with direct intersection")
