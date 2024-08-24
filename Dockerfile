# Use the official Airflow image from the Apache Airflow project as the base image
FROM apache/airflow:2.7.1-python3.9

# Set environment variables for Airflow
ENV AIRFLOW_HOME=/opt/airflow

# Install any additional Python packages required for your workflows
# For example, if you need to add extra packages for data processing or database connections
RUN pip install --no-cache-dir \
    pandas \
    sqlalchemy \
    requests \
    google-cloud-storage \
    # Add other packages here

# Copy any custom Airflow plugins, configurations, or scripts into the image
# Assuming you have a custom plugin directory and Airflow configuration files
COPY ./plugins /opt/airflow/plugins
COPY ./dags /opt/airflow/dags
COPY ./config/airflow.cfg /opt/airflow/airflow.cfg

# Expose the port on which Airflow web server runs
EXPOSE 8080

# Set the default command to start Airflow
CMD ["airflow", "webserver"]
