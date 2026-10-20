# Portfolio submission

## Project title
Customer Data Quality Validation Pipeline with PySpark and PyDeequ

## Two-sentence introduction
I built a Docker-based customer-data validation project using native PySpark transformations and PyDeequ verification and profiling. The demonstrated run identifies duplicate customer IDs, missing ages, and invalid age bounds, with saved JSON reports that reviewers can inspect and reproduce.

## Links
- [Project and source](https://github.com/Rems2014/rems2014.github.io/tree/main/projects/data-quality)
- [Portfolio](https://rems2014.github.io/)
- [Author](https://github.com/Rems2014)

## Reviewer walkthrough
1. Read the README for architecture, scope, decisions, and limitations.
2. Inspect examples/verification.json: completeness passes; uniqueness and both age bounds fail intentionally.
3. Inspect examples/metrics.json: size 4, uniqueness 0.5, mean age about 56.67.
4. Trace each check in Data_quality.py.
5. Run docker compose run --build --rm data-quality from the project folder.
6. Run python -m unittest discover -s tests -v to check new reports.
7. Review the latest GitHub Actions run.

## Engineering reflection
The practical challenge was making the runtime reproducible while distinguishing data-quality findings from application failures. Docker isolated Spark, Java, and PyDeequ from conflicting Windows Python packages. Native DataFrame operations express the checks in Spark, and saved reports make findings inspectable. Future enforcement must define record-level rejection rules explicitly; dataset-level failed checks alone do not provide quarantine routing.

## Evidence boundary
The evidence is a synthetic four-record local run. Airflow, external ingestion, Medallion storage, quarantine, performance improvements, and production business impact are planned rather than demonstrated.
