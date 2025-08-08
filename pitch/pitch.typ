#import "@preview/peace-of-posters:0.5.6" as pop

#set page("a0", margin: 1cm)
#pop.set-poster-layout(pop.layout-a0)
#set text(font: "Arial", size: pop.layout-a0.at("body-size"))

#let box-spacing = 1.2em
#set columns(gutter: box-spacing)
#set block(spacing: box-spacing)
#pop.update-poster-layout(spacing: box-spacing)

#let scr(it) = text(
  features: ("ss01",),
  box($cal(it)$),
)

#set math.equation(numbering: "(1)")

#pop.set-theme(pop.uni-fr)

#pop.title-box(
  "Mathematical Notions of Cellular Agent-Based Models",
  authors: "Jonas Pleyer¹, Christian Fleck¹",
  institutes: "¹Freiburg Center for Data-Analysis, Modeling and AI"
)

#columns(2, [
  #pop.common-box(
    heading: "What are Cellular ABMs?",
    body: [#figure(stack(dir: ttb, [
      #place(top+left, rect(inset: 5pt)[*A*])
      #grid(columns: 3,
        image("../figures/cells_at_iter_0000000200.png"),
        image("../figures/cells_at_iter_0000003400.png"),
        image("../figures/cells_at_iter_0000006600.png"),
      )],[
      #place(top+left, rect(inset: 5pt)[*B*])
      #grid(columns: 2,
        inset: (top: 30pt, bottom: -50pt),
        image("../figures/bacterial-rods/0000000025.png", fit: "cover", width: 100%, height: 7em),
        image("../figures/bacterial-rods/0000007200.png", fit: "cover", width: 100%, height: 7em),
        // image("../figures/bacterial-rods/0000015000.png"),
      )]
    ),
    caption: [
      (A) Time Series of growing bacterial colony which forms a spatial pattern.
      (B) Rod-Shaped bacteria grow inside a confined space and align themselves along the elongated
      axis of direction.
      The individual behaviour of agents results in complex collective phenomena.
    ])
    - Describe cells individually
    - Cells interact with each other and domain
  ],
    stretch-to-next: true,
  )

  #colbreak()

  /* #pop.common-box(
    heading: "Comparing ABM Frameworks",
    body: grid(align: (left, center, center, center), columns: 4, inset: 20pt,
    stroke: (x, y) => {
      if y==1 {(top: (paint: black, thickness: 2pt))}
    },
      [*ABM*],[*Mathematical Formulation*],[*Individual-Based*],[*Extensibility*],
      [Biocellion],[❌],[✅],[],
      [BSim],[?],[✅],[],
      [CompuCell3D],[✅],[❌],[],
      [EPISIM],[],[],[],
      [Morpheus],[?],[(✅)],[],
      [MultiCellSim],[],[],[],
      [PhysiCell],[✅],[✅],[],
      [TSim/CellSys],[],[],[],
      [VirtualLeaf],[],[],[],
    ),
  )*/

  #pop.common-box(
    heading: "Shared Concepts",
    body: grid(align: left, columns: 3, inset: 20pt,
    stroke: (x, y) => {
      if y==2 {(top: (paint: black, thickness: 2pt))}
      if y==9 {(top: (paint: black, thickness: 2pt))}
      if y==12 {(top: (paint: black, thickness: 2pt))}
    },
      [],[*Aspect*],[*Examples*],
      [],[*(C) Single-Cell*],[],
      [(1)],[Mechanics],[Spherical, Rod-Shaped, Hexagonal],
      [(2)],[Growth],[Extension along Rod, Spherically],
      [(3)],[Division],[Binary Fision, Mitosis & Meiosis],
      [(4)],[Reactions],[Metabolism, Signalling],
      [(5)],[Differentiation],[Muscle, Fat, Epithelial Cells],
      [(6)],[Individual Parameters],[Distribution of Growth Rates],
      [],[*(CC) Cell-Cell*],[],
      [(7)],[Forces],[Adhesion, Friction],
      [(8)],[Reactions],[Gap Junctions],
      [],[*(DC) Domain-Cell*],[],
      [(9)],[External Forces],[Microfluidics, Adhesion],
      [(10)],[Extracellular Reactions],[Diffusion, Nutrient Uptake],
    ),
  )
])

#columns(2, [
  #pop.common-box(
    heading: [Mathematical Formulation],
    body: [
      == Cellular State
      Cells live inside a space $C$.
      We ensure the individuality via a unique index $iota in I$ per cell $c_iota$.
      This index can only be used by this particular cell and no other (following or preceding).

      == Cellular Space $scr(C)$
      $ scr(C) = \{ M in underbrace(text("Pot")(I), "used indices") times
        underbrace(text("Pot")(I times C), "current state") | M text("is cellular state") \} $
      Combine with domain $scr(D)$ and evolution function $phi.alt =>$ dynamical system
      $ M = scr(C) times scr(D) $

      == Dynamics
      - Single Division function: mapping $gamma: C -> union_(n gt.eq 2) C^n$
      - Motion: Newtonian, Brownian, Langevin $dot.double(x) = dots$
      - 
    ]
  )

  #pop.common-box()

  #colbreak()

  #pop.common-box()
  #pop.common-box()
])
