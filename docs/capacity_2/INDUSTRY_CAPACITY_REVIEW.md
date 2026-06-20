# INDUSTRY CAPACITY REVIEW

Project: V7 VOZDUH
Program: CAPACITY.2_OBSERVED_CAPACITY_MODEL_AUDIT
Mode: audit only
Last verified commit: `67fbd8506321802222c6f8ed3d34cfe406a45d8a`

## Sources Reviewed

- Google SRE Book, capacity planning and monitoring chapters: https://sre.google/sre-book/software-engineering-in-sre/ and https://sre.google/sre-book/monitoring-distributed-systems/
- AWS EC2 Auto Scaling target tracking: https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-target-tracking.html
- Kubernetes Horizontal Pod Autoscaler: https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/
- Cloudflare Load Balancing traffic steering: https://developers.cloudflare.com/load-balancing/understand-basics/traffic-steering/

## Findings

| System | Pattern | Relevance to V7 |
| --- | --- | --- |
| Google SRE | Capacity planning is not static only; it uses demand forecasts, performance metrics, dependencies, and ongoing revision. Monitoring focuses on latency, traffic, errors, and saturation. | V7 should use observed symptoms, not only configured limits, when learning practical capacity. |
| AWS Auto Scaling | Target tracking adjusts capacity based on metrics and target values; multiple metrics can provide more information about load. | Static thresholds are safety rails; metric-driven behavior is the scalable pattern. |
| Kubernetes HPA | Control loop adjusts desired scale from observed metrics such as CPU, memory, or custom metrics. | V7 can safely start with custom observed tunnel-quality metrics in shadow mode. |
| Cloudflare Load Balancing | Traffic steering starts from pool/endpoint health and redistributes when pools/endpoints become unhealthy. | V7 should treat service/runtime health as a primary observable before routing/assignment recommendations. |

## Answer

Successful production systems do not rely on static limits only.

They combine:

- configured bounds;
- observed health;
- observed demand;
- latency/error/saturation symptoms;
- conservative control loops;
- safety buffers and warmup/cooldown logic.

## V7 Interpretation

For V7, static limits remain required because V7 often does not own the underlying tunnel. But observed degradation should become a shadow learning layer because V7 does observe service quality, speed, latency, stability, fail rate, runtime readiness, history, and assigned users.

## Audit Verdict

Industry practice supports an observed-capacity shadow model. It does not support immediately replacing planner limits with unproven learned thresholds.
