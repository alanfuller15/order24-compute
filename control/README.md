# control/

`control/HOLD`: when this file exists, `.github/workflows/refill.yml` dispatches nothing (kill switch). The refill creates it
itself when any log or result shows ORIGINAL_MODEL_FOUND (details in `ops/ALERT`). Only the manager removes it, after the
model has been examined. A model is never resumed past.
