import os
import sys
from pathlib import Path
import json

os.environ["SPARK_VERSION"] = "3.5.0"
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
# Java is configured by the Docker image.

from pyspark.sql import SparkSession

from pyspark.sql.functions import col, when, count, current_date, datediff, to_date

import pydeequ

from pydeequ.checks import Check, CheckLevel
from pydeequ.verification import VerificationSuite, VerificationResult
from pydeequ.analyzers import AnalysisRunner, AnalyzerContext, Uniqueness, Mean, Size


def main():
    # Initialize Spark Session with PyDeequ dependencies
    spark = (
        SparkSession.builder.master("local[2]").appName("DataQualityLearnerComplete")
        .config("spark.jars.packages", pydeequ.deequ_maven_coord)
        .config("spark.jars.excludes", pydeequ.f2j_maven_coord)
        .getOrCreate()
        
    )
    
    try:
        report_dir = Path(os.environ.get("REPORT_DIR", "reports"))
        report_dir.mkdir(parents=True, exist_ok=True)
        
        # Sample dataset
        df = spark.createDataFrame([
            (1, "Alice", 25, "12345", "2026-08-01"),
            (2, "Bob", None, "99999", "2026-05-01"),
            (2, "Bob", 150, "99999", "2026-05-01"),
            (3, "Charlie", -5, "54321", "2026-08-04"),
            
        ], 
        ["customer_id", "name", "age", "postal_code", "last_updated"])
        
        reference_df = spark.createDataFrame([
            (1, "12345"),
            (2, "99999"),
            (3, "54321"),
        ], 
        ["id", "postal_code"])
        
        df1 = spark.createDataFrame([
            (1, "alice@email.com"),
            (2, "bob@email.com")],
            ["customer_id", "email"])
        
        df2 = spark.createDataFrame([
            (1, "alice@email.com"),
            (2, "bob_old@email.com")],
            ["customer_id", "email"])
        
        # 1. Completeness: count missing values in 'age'
        print("--- 1.0 completeness check for 'age' column ---")
        df.select([count(when(col("age").isNull(), 1)).alias("missing_age_count")]).show()
        
        
        # 2. Uniqueness: count duplicate values in 'customer_id'
        print("--- 2.0 Uniqueness check for 'customer_id' column ---")
        df.groupBy("customer_id").count().filter("count > 1").show()
        
        # 3. Validity
        print("--- 3.0 Value Constraints (Domain) check for 'age' ---")
        df.filter(col("age") < 0).show()
        df.filter(col("age") > 120).show()
        
        # 4. Accuracy: match against reference dataset and filter postal code discrepancies
        print("--- 4.0 Accuracy (compare with reference_df) ---") 
        df.join(reference_df,     df["customer_id"] == reference_df["id"]).filter(df["postal_code"] != 
        reference_df["postal_code"]).show()
        
        
        # 5. Consistency: Join df1 and df2 on customer_id to spot conflicting emails
        print("--- 5.0 Consistency (compare df1 and df2) ---")
        df1.join(df2, "customer_id").filter(df1["email"] != df2["email"]).show()
        
        
        # 6. Timeliness: flags records older than 30 days
        print("---6.0  Timeliness ---")
        df.withColumn("stale_data", datediff(current_date(), to_date(col("last_updated"))) > 30).show()
        
        # 7 PyDeequ Constraints Verification
        print("--- 7.0 PYDEEQU CONSTRAINTS AUDIT ---")
        check = Check(spark, CheckLevel.Error, "Learner validation Check")
        check_result = (
            VerificationSuite(spark)
            .onData(df)
            .addCheck(
                check.hasCompleteness("age", lambda x: x >= 0.75)
                .isUnique("customer_id")
                .hasMin("age", lambda x: x >= 0)
                .hasMax("age", lambda x: x <= 120)
            )
            .run()
        )
        audit_df = VerificationResult.checkResultsAsDataFrame(spark, check_result)
        audit_df.show(truncate=False)
        (report_dir / "verification.json").write_text(json.dumps([json.loads(row) for row in audit_df.toJSON().collect()], indent=2), encoding="utf-8")
        
        # 8. Pydeequ AnalysisRunner Profiling
        print("--- 8.0 PYDEEQU PROFILING METRICS---")
        analysis_result = (
            AnalysisRunner(spark)
            .onData(df)
            .addAnalyzer(Size())
            .addAnalyzer(Uniqueness(["customer_id"]))
            .addAnalyzer(Mean("age"))
            .run()
        
        )
        metrics_df = AnalyzerContext.successMetricsAsDataFrame(spark, analysis_result)
        metrics_df.show(truncate=False)
        (report_dir / "metrics.json").write_text(json.dumps([json.loads(row) for row in metrics_df.toJSON().collect()], indent=2), encoding="utf-8")
        
        print(f"Reports saved to {report_dir.resolve()}")
    finally:
        # PyDeequ starts a Python callback server for constraint lambdas.
        # Close it explicitly so the container can exit after the audit.
        gateway = spark.sparkContext._gateway
        try:
            spark.stop()
        finally:
            if gateway is not None:
                gateway.shutdown_callback_server()


if __name__ == "__main__":
    main()
