# classicalSims

This repository is for classically simulation current phase relations (CPRs) of common circuits.
In particular, this application is meant to be interfaced through the scr/main.py function to
simulate all varieties of "leg" circuits (a JJ in series with a inductor)

- Can be programatically interfaced with via command line arguments or YAML config files.

Notes:

- The behavior of the linear rhombus simulations at coarse grid sizes and small EJ/EL is just an artifact of the gridding in the current dimension. Not a concern.

- The linear rhombus on it's own has a compact phase --  the phi variable + 2pi doesn't enter the hamiltonian anywhere. HOWEVER, in the GKP circuit, it does, and therefore the non-compatness there is relevant and should be accounted for (calculating multiple periods).

TODO:

[ ] Test

[ ] Calculate the minimum of each curve and label it as stable or not.

[ ] Plot the existance (or lack thereof) of the minima in each case.

[ ] Confirm stability is being calculated correctly on the atomic scale (i.e. for each leg -- seems fine for combined).

[ ] Contiguous curve finder that also smooths or averages the curves so that minima and other operations can be done (would be nice to feed these into quantum sims for example)

[ ] Function for circulating current rather than net linear flow.

[ ] 