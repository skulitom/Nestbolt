# Draft issue for JeroenGar/sparrow (not posted)

**Title:** Guided-local-search weights have no ceiling and overflow f32 (`weighted loss should never increase: ∞ > NaN`)

---

### Summary

`CollisionTracker::update_weights` (`src/quantify/tracker.rs`) multiplies the
weight of every colliding entry by 1.2–2.0 per iteration and decays the others
by 0.95, with a floor of 1.0 but no ceiling. `restore_but_keep_weights` keeps
the weights across rollbacks. When compression asks for a strip that cannot be
feasible, one pair can collide on enough consecutive iterations for its weight
to pass `f32::MAX` (about 3.4e38). The weight becomes `∞`, and `∞ × 0.95` is
still `∞`, so it never decays. Once that pair separates, its weighted loss is
`∞ × 0 = NaN`. In debug builds this trips the assertion in
`SeparatorWorker::move_item`.

### Reproduction (sparrow `4629b22`, jagua-rs 1.1.0, debug build)

`three-squares.json`: three 2×2 squares in a strip of height 5. The optimum is
length 4, and compression keeps trying shorter strips.

```json
{
  "name": "three-squares",
  "items": [
    {
      "id": 0,
      "demand": 3,
      "orientation": {"rotation": {"mode": "discrete", "angles": [0, 90]}},
      "shape": {"type": "rectangle", "data": {"x_min": 0.0, "y_min": 0.0, "width": 2.0, "height": 2.0}}
    }
  ],
  "strip_height": 5.0
}
```

```
cargo run --bin sparrow -- -i three-squares.json -t 60 -s 0
```

Observed on Windows x86-64 with rustc 1.98.1: after 20–30 s, three worker
threads panic with

```
thread '<unnamed>' panicked at src\optimizer\worker.rs:87:9:
weighted loss should never increase: ∞ > NaN
```

Seed 1 ran its 30 s without panicking. In a copy instrumented to log weights
(same geometry, run through a downstream adapter), one pair entry climbed
through 1e30–1e36 before the panic, with its loss alternating between about
0.37 and 0 from one iteration to the next.

### Why it matters beyond debug builds

Release builds compile the assertion out, so a weight that reaches `∞` stays
there for the rest of the run, and every overlap with that partner then scores
the same. A faster collision engine reaches the overflow sooner. With jagua-rs
`main` after #125, the same input triggers it in about 0.15 s in a debug build,
against 2.29 s on 1.1.0. In a multi-sheet adaptation of this separator using
the same update rule, a benchmark instance (blaz1, multiple bins) reached
weights of 1e34 within about a minute of search.

### Suggested fix

Clamp the weights, for example

```rust
e.weight = (e.weight * multiplier).clamp(1.0, 1e20);
```

With at most 64 poles per surrogate, a pair loss stays below about `80·d²` for
parts of diameter `d`. So a ceiling of 1e20 keeps weighted losses and their sums
far below `f32::MAX` at any realistic scale. Rescaling all weights when the
largest passes a threshold would also work.
