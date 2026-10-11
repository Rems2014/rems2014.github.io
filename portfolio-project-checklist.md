# Data Engineering Portfolio Project Checklist

Mupembe Tshisekedi — Personal Data Engineering Portfolio

## Define the problem
- [ ] Explain the business question and intended data consumer.
- [ ] State dataset provenance, licensing, and limitations.
- [ ] Label synthetic data and simulated workloads clearly.

## Build the system
- [ ] Show source → ingestion → storage → transformation → consumption.
- [ ] Define table grain, keys, schema, and incremental load behavior.
- [ ] Handle retries, duplicate records, late data, and safe re-runs.
- [ ] Keep credentials out of the repository.

## Verify it
- [ ] Test keys, nullability, relationships, and business rules.
- [ ] Demonstrate one deliberately introduced failure and recovery.
- [ ] Record actual performance measurements with configuration and hardware.
- [ ] Document freshness checks, monitoring, and operational responsibilities.

## Present the evidence
- [ ] Provide a repository with pinned dependencies and sample configuration.
- [ ] Write a setup guide another person can follow.
- [ ] Include an architecture diagram, screenshots, and test output.
- [ ] Explain tradeoffs, known limitations, and next improvements.
- [ ] Separate completed work from future plans.

## Learning resources
- DataTalksClub: https://github.com/DataTalksClub/data-engineering-zoomcamp
- PostgreSQL: https://www.postgresql.org/docs/current/tutorial.html
- Airflow: https://airflow.apache.org/docs/
- dbt: https://docs.getdbt.com/
- Spark: https://spark.apache.org/docs/latest/
- Microsoft Learn: https://learn.microsoft.com/en-us/training/paths/get-started-data-engineering/

## Batch Processing & Cloud Migration Pipelines
- [ ] Demonstrate full backfill and incremental loading.
- [ ] Reconcile source and target counts, checksums, and schemas.
- [ ] Document cutover, rollback, access controls, and cloud costs.

## Real-Time Streaming & Event-Driven Pipelines
- [ ] Explain event schemas, partition keys, and ordering assumptions.
- [ ] Demonstrate late events, deduplication, and checkpoint recovery.
- [ ] Implement retries, dead-letter handling, and replay.
- [ ] Measure consumer lag and end-to-end latency.

### Additional resources
- Kafka: https://kafka.apache.org/documentation/
- Azure Data Factory: https://learn.microsoft.com/en-us/azure/data-factory/introduction
