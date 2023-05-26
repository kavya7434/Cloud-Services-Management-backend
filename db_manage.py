import psycopg2
import json


class Db_management:
    sqlURL = 'postgres://hjughgcw:FyaH8aZH0oRL6txJXy8pkKCitLy9_mpy@tiny.db.elephantsql.com/hjughgcw'
    dto = {
        "sideNav": {
            "categories": [
                {
                    "name": "Compute Services",
                    "services": [
                        {
                            "name": "Virtual Machines",
                            "link": "/virtual-machines"
                        },
                        {
                            "name": "Serverless Compute",
                            "link": "/serverless-compute"
                        },
                        {
                            "name": "Kubernetes Engines",
                            "link": "/kubernetes-engines"
                        }
                    ]
                },
                {
                    "name": "Networking",
                    "services": [
                        {
                            "name": "VPC",
                            "link": "/vpc"
                        },
                        {
                            "name": "Load Balancing",
                            "link": "/load-balancing"
                        }
                    ]
                },
                {
                    "name": "Storage Services",
                    "services": [
                        {
                            "name": "Object Storage",
                            "link": "/object-storage"
                        },
                        {
                            "name": "Databases",
                            "link": "/databases"
                        },
                        {
                            "name": "File Storage",
                            "link": "/file-storage"
                        },
                        {
                            "name": "Block Storage",
                            "link": "/block-storage"
                        }
                    ]
                },
                {
                    "name": "Big Data",
                    "services": [
                        {
                            "name": "Spark/Hadoop Service",
                            "link": "/spark-hadoop-service"
                        },
                        {
                            "name": "Streaming Service",
                            "link": "/streaming-service"
                        }
                    ]
                },
                {
                    "name": "Security and Identity Management",
                    "services": [
                        {
                            "name": "Identity & Access Management",
                            "link": "/identity-access-management"
                        }
                    ]
                },
                {
                    "name": "Operations Tools",
                    "services": [
                        {
                            "name": "Metrics Monitoring",
                            "link": "/metrics-monitoring"
                        },
                        {
                            "name": "Logging",
                            "link": "/logging"
                        }
                    ]
                }
            ]
        }
    }
    def __init__(self):
        self.connection = psycopg2.connect(self.sqlURL)
        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute("CREATE TABLE IF NOT EXISTS categories (name TEXT PRIMARY KEY);")
                    cursor.execute(
                        "CREATE TABLE IF NOT EXISTS services (id SERIAL PRIMARY KEY, name TEXT, category_name TEXT, FOREIGN KEY (category_name) REFERENCES categories(name) ON DELETE CASCADE, UNIQUE (name, category_name));")
                    cursor.execute(
                        "CREATE TABLE IF NOT EXISTS fields (id SERIAL PRIMARY KEY, name TEXT, value TEXT, type TEXT, category_name TEXT, service_name TEXT, FOREIGN KEY (category_name) REFERENCES categories(name) ON DELETE CASCADE, FOREIGN KEY (service_name, category_name) REFERENCES services(name, category_name) ON DELETE CASCADE);")

                    # Insert categories if they don't already exist
                    categories = self.dto['sideNav']['categories']
                    for category in categories:
                        category_name = category['name']
                        try:
                            cursor.execute("INSERT INTO categories (name) VALUES (%s)", (category_name,))
                        except psycopg2.errors.UniqueViolation:
                            print(f"Category '{category_name}' already exists. Skipping insertion.")
                            self.connection.rollback()

                    # Insert services if they don't already exist
                    services = [service for category in categories for service in category['services']]
                    for service in services:
                        service_name = service['name']
                        category_name = next(
                            category['name'] for category in categories if service in category['services'])
                        try:
                            cursor.execute("INSERT INTO services (name, category_name) VALUES (%s, %s)",
                                           (service_name, category_name))
                        except psycopg2.errors.UniqueViolation:
                            print(
                                f"Service '{service_name}' under category '{category_name}' already exists. Skipping insertion.")
                            self.connection.rollback()

                    self.connection.commit()
        except psycopg2.errors.DuplicateTable:
            pass

    def get_dto(self):
        conn = psycopg2.connect(self.sqlURL)
        cursor = conn.cursor()

        # Retrieve categories
        cursor.execute("SELECT name FROM categories")
        categories = cursor.fetchall()

        dto = {
            "sideNav": {
                "categories": []
            }
        }

        # Iterate over categories
        for category in categories:
            category_name = category[0]

            # Retrieve services for each category
            cursor.execute("SELECT name FROM services WHERE category_name = %s", (category_name,))
            services = cursor.fetchall()

            # Create category entry in dto
            category_entry = {
                "name": category_name,
                "services": []
            }

            # Iterate over services
            for service in services:
                service_name = service[0]

                # Retrieve fields for each service
                cursor.execute("SELECT name, value, type FROM fields WHERE service_name = %s AND category_name = %s",
                               (service_name, category_name))
                fields = cursor.fetchall()

                # Create service entry in category
                service_entry = {
                    "name": service_name,
                    "fields": []
                }

                # Iterate over fields
                for field in fields:
                    field_name, field_value, field_type = field
                    field_entry = {
                        "name": field_name,
                        "value": field_value,
                        "type": field_type
                    }

                    # Add field entry to service
                    service_entry["fields"].append(field_entry)

                # Add service entry to category
                category_entry["services"].append(service_entry)

            # Add category entry to dto
            dto["sideNav"]["categories"].append(category_entry)

        conn.close()

        return dto

    def get_cat_services(self):
        conn = psycopg2.connect(self.sqlURL)
        cursor = conn.cursor()

        # Retrieve categories
        cursor.execute("SELECT name FROM categories")
        categories = cursor.fetchall()

        dto = {
            "sideNav": {
                "categories": []
            }
        }

        # Iterate over categories
        for category in categories:
            category_name = category[0]

            # Retrieve services for each category
            cursor.execute("SELECT name FROM services WHERE category_name = %s", (category_name,))
            services = cursor.fetchall()

            # Create category entry in dto
            category_entry = {
                "name": category_name,
                "services": []
            }

            # Iterate over services
            for service in services:
                service_name = service[0]

                # Create service entry in category
                service_entry = {
                    "name": service_name
                }

                # Add service entry to category
                category_entry["services"].append(service_entry)

            # Add category entry to dto
            dto["sideNav"]["categories"].append(category_entry)

        conn.close()

        return dto

    def get_fields(self, category_name, service_name):
        conn = psycopg2.connect(self.sqlURL)
        cursor = conn.cursor()

        cursor.execute("SELECT name, value, type FROM fields WHERE category_name = %s AND service_name = %s",
                       (category_name, service_name))
        fields = cursor.fetchall()

        result = []
        for field in fields:
            field_name, field_value, field_type = field
            result.append({
                "name": field_name,
                "value": field_value,
                "type": field_type
            })

        conn.close()

        return result

    def delete_category(self, category_name):
        conn = psycopg2.connect(self.sqlURL)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM services WHERE category_name = %s", (category_name,))
        cursor.execute("DELETE FROM fields WHERE category_name = %s", (category_name,))
        cursor.execute("DELETE FROM categories WHERE name = %s", (category_name,))

        conn.commit()
        conn.close()
        return "category removed successfully"

    def add_category(self, category_name):
        conn = psycopg2.connect(self.sqlURL)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO categories (name) VALUES (%s)", (category_name,))
            conn.commit()
            conn.close()
            return "Category added successfully!"
        except psycopg2.errors.UniqueViolation:
            return "Category already exists!"
        finally:
            conn.close()

    def delete_service(self, category_name, service_name):
        conn = psycopg2.connect(self.sqlURL)
        cursor = conn.cursor()

        # Delete fields associated with the service
        cursor.execute("DELETE FROM fields WHERE service_name = %s AND category_name = %s",
                       (service_name, category_name))

        # Delete the service
        cursor.execute("DELETE FROM services WHERE name = %s AND category_name = %s", (service_name, category_name))

        conn.commit()
        conn.close()
        return "service removed successfully"

    def add_service(self, category_name, service_name):
        conn = psycopg2.connect(self.sqlURL)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO services (name, category_name) VALUES (%s, %s)", (service_name, category_name))
            conn.commit()
            conn.close()
            return "Service added successfully!"
        except psycopg2.errors.UniqueViolation:
            conn.close()
            return "Service already exists!"
        finally:
            conn.close()

        # return service_id

    def add_field(self, category_name, service_name, field_name, field_value, field_type):
        conn = psycopg2.connect(self.sqlURL)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO fields (name, value, type, category_name, service_name) VALUES (%s, %s, %s, %s, %s)",
            (field_name, field_value, field_type, category_name, service_name))
        conn.commit()
        conn.close()
        return "field added successfully"

    def delete_field(self, category_name, service_name, field_name):
        conn = psycopg2.connect(self.sqlURL)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM fields WHERE category_name = %s AND service_name = %s AND name = %s",
                       (category_name, service_name, field_name))
        conn.commit()
        conn.close()
        return "field removed successfully"

    def update_field(self, category_name, service_name, field_name, new_value):
        conn = psycopg2.connect(self.sqlURL)
        cursor = conn.cursor()

        # Update the field value
        cursor.execute("UPDATE fields SET value = %s WHERE service_name = %s AND category_name = %s AND name = %s",
                       (new_value, service_name, category_name, field_name))

        conn.commit()
        conn.close()
        return "field updated successfully"


