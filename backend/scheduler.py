# import time
# import subprocess
# import logging

# # Set up logging
# logging.basicConfig(
#     filename="hr_scheduler.log",
#     filemode="a",
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     level=logging.INFO,
# )

# hr_file_path = "hr_main.py"
# hr_time = "20:04"  # Set the desired schedule time for the HR script

# def run_hr_program():
#     logging.info("Starting scheduled HR job")
#     try:
#         subprocess.run(
#             ["python", hr_file_path],
#             check=True,
#         )
#         logging.info("HR ETL completed successfully")
#     except subprocess.CalledProcessError as e:
#         logging.error(f"HR ETL failed due to error {e}")

# # Schedule the job
# schedule.every().day.at(hr_time).do(run_hr_program)

# interval = 4
# for i in range(int)
# schedule.every().minutes.

# logging.info("HR Scheduler started")

# # Keep the script running
# try:
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
# except KeyboardInterrupt:
#     print("\nScript terminated by user.")
