# Reproducibility Checklist

- Code entry point: `src/run_experiment.py`
- Requirements: `numpy`, `matplotlib`
- Deterministic base seed: `12040615`
- Main outputs:
  - `results/seed_task_regime_metrics.csv`
  - `results/seed_split_metrics.csv`
  - `results/metrics.csv`
  - `results/pairwise_stats.csv`
  - `results/ablation_metrics.csv`
  - `results/stress_sweep.csv`
  - `results/failure_cases.csv`
  - `results/summary.txt`
- Main figures:
  - `figures/belief_revision_intervention_combined_success.png`
  - `figures/belief_revision_intervention_diagnostics.png`
  - `figures/belief_revision_intervention_stress_sweep.png`
  - `figures/belief_revision_intervention_ablation.png`
  - `figures/belief_revision_intervention_regime_gains.png`

Reproduction command:

```powershell
pip install -r requirements.txt
python src\run_experiment.py
```
