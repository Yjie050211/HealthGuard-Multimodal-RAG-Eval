# ST-GCN Reproduction Boundary

Current status: **not implemented in this code snapshot**.

## What can be said truthfully

- ST-GCN models human skeleton sequences as spatio-temporal graphs.
- A typical input tensor is `N x C x T x V x M`:
  - `N`: number of samples
  - `C`: coordinate/confidence channels
  - `T`: time frames
  - `V`: skeleton joints
  - `M`: number of people
- ST-GCN is a reasonable future baseline for fall or behavior recognition if skeleton keypoints are available.

## What cannot be claimed yet

- No ST-GCN training has been run.
- No ST-GCN inference result exists.
- No skeleton keypoint sequence dataset exists in this project.
- No open-source ST-GCN repository has been integrated.

## Next reproducible step

1. Select a maintained open-source ST-GCN implementation.
2. Record the paper and repository source.
3. Prepare a tiny skeleton sequence sample.
4. Run one inference or toy training command.
5. Save logs, config, predictions, and exact environment notes.
