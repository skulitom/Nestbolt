# Draft issue for JeroenGar/jagua-rs (not posted)

**Title:** `offset_shape` is no longer a superset (inflate) or subset (deflate) when the offset is small: `SPolygon::new` removes the round-join vertices

---

### Summary

jagua-rs 2.0.0 builds every polygon through `SPolygon::new`, which removes each
vertex closer than `MIN_EDGE_LENGTH_RATIO` (1e-5) times the diameter to the
previous kept vertex. `offset_shape_once` passes the buffered outline through
the same constructor. When the offset distance is of the order of that minimum
edge length, the vertices of a corner's round join lie closer together than
the minimum, so the join collapses to its first vertex. The next edge then runs
from that vertex to the far end of the following offset edge. At a right angle
this edge starts on the original outline: the inflated shape keeps no margin at
that end of the edge. By the same geometry a sharper corner would put it
inside the original; that case was not reproduced here.

`Importer::with_min_item_separation` documents that items are inflated and
containers deflated by half the distance, and `offset_shape`'s own comment
expects a retried offset to remain a superset (inflate) or subset (deflate) of
the original. After the removal the result is still a superset in this
example, but with no margin left along parts of it. 1.1.0 kept every buffered
vertex.

### Reproduction (jagua-rs 2.0.0 from crates.io)

An L-shape about 4 units across, imported with `min_item_separation = 2.9e-5`
(offset 1.45e-5; the shape's minimum edge length is 5e-5):

```rust
let pts = vec![(0.0, 0.0), (4.0, 0.0), (4.0, 1.0), (1.0, 1.0), (1.0, 3.0), (0.0, 3.0)];
let importer = Importer::new(CDEConfig { item_surrogate_config: SPSurrogateConfig::none() }, None, None)
    .with_min_item_separation(2.9e-5)?;
let item = importer.import_item(&ExtItem {
    id: 0,
    orientation: ExtOrientation { rotation: ExtRotation::Continuous {}, reflection_axes: vec![] },
    shape: ExtShape::SimplePolygon(ExtSPolygon(pts)),
    min_quality: None,
}, 0)?;
println!("{:?}", item.shape_cd().vertices());
```

The original, in the item's centred frame, is
`(-1.5, -1) (2.5, -1) (2.5, 0) (-0.5, 0) (-0.5, 2) (-1.5, 2)`.
The collision shape has six vertices:

```
(-1.5000145, 2.0) (-1.5000145, -1.0) (2.5, -1.0000145)
(2.5000145, -2.2e-16) (-0.49998552, 1.45e-5) (-0.49998552, 2.0)
```

Its top edge lies on the original top edge (`y = 2.0`), and the bottom and
right edges touch the original at one end each. With separations of 1e-4,
4e-4 and 1e-3 the shape has 11, 31 and 46 vertices: the joins are thinned but
survive.

### Effect

Two items placed in contact by their collision shapes can overlap in their
original outlines. Nestbolt found this on the Blazewicz instance with zero
spacing: its independent Clipper2 check rejected one to eight of every eighty
constructed trial layouts, each with an overlap of about 4e-6 of a part's area.
With 1.1.0 the same runs had none.

### Possible fixes

- Build the offset result without short-edge removal, or reject and retry with
  a larger distance (as the self-intersection retry already does) when removal
  would drop a vertex.
- Offset small distances with mitred joins, which add no short edges.
- Document a minimum useful offset relative to the diameter.

Nestbolt now requests a larger separation, sized from the part and sheet
diameters, so that the margin it needs survives the removal
(`engine_separation` in `crates/core/src/construct.rs`).
