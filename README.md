# 🏎️ F1-ENE-datapipeline-project

This is a December Decision series where I try to show my skills of Data Engineer. A detailed documentation of the cloud data lake design, setup, and security implementation completed so far.

## 📘 Project Overview

This project aims to design, secure, and structure a Cloud Data Lake using Azure ADLS Gen2 following industry standards such as:

Azure Resource Organization

Medallion Architecture (Bronze/Silver/Gold)

Key Vault for secrets management

IAM/RBAC for secure access control

Storage Firewalls & Network Restrictions

## Goal

The goal is to design a end to end data pipeline that pulls data from the API and get store data in medallion architecture. Using python script to transform data into clean data and ready to use by Data analyst and Data engineer.

## ✅ Progress Completed So Far

This section documents every cloud engineering step completed up to now.

1. Azure Account Setup

    Created an Azure account and free-tier subscription.
    Configured access to Azure Portal and Azure CLI environment.

2.Created Resource Group

    A Resource Group (RG) was created to logically organize all project resources.

    Purpose:

        Helps manage resources as a single unit
        Enables grouped RBAC permissions
        Supports consistent deployment & cleanup

3.Created Azure Storage Account (ADLS Gen2 Enabled)

    A Storage Account was created with:
    Hierarchical Namespace = ON → required for ADLS Gen2
    Region aligned with the Resource Group
    Standard redundancy settings

    Purpose:

        Store the raw and processed F1 datasets
        Form the foundation of the data lake

4.Created a Container for Data Lake Storage

    Inside the Storage Account, a container was created.

    Containers act like “root directories” for organizing storage.

5.Created Sub-Folders Using Medallion Architecture

    Following industry best practices, the following folder structure was created inside the container:

    datalake/
    │
    ├── bronze/   → Raw ingestion zone
    ├── silver/   → Cleaned & standardized data
    └── gold/     → Curated, analytics-ready data

    Purpose of the layers:

        Layer Description
        Bronze Stores unmodified raw F1 data
        Silver Cleaned, structured datasets ready for joins
        Gold Final business tables for reporting/analytics

    This structure ensures maintainability, traceability, and clarity.

6.Created an Azure Key Vault

    A Key Vault was created to manage credentials and secrets.

    Purpose:

        Store Storage Account keys
        Store SQL credentials (future use)
        Eliminate sensitive data in code
        Integrate with future services (ADF, Databricks, Functions)

        Key Vault capabilities enabled:
            Secret storage
            Secure access policies
            RBAC integration

7.Added IAM Roles for Secure Access Control

    Role-Based Access Control (RBAC) was configured on the Storage Account.

    Assigned Role:

        ✔ Storage Blob Data Contributor → Assigned to my user account

    Reason:
        Allows uploading, modifying, deleting files within ADLS while preventing resource-level administrative actions.

8. Initial Network & Security Setup

    The following network security configurations were applied:
        ✔ Enabled “Selected Networks”

    Public access is restricted to:
       My IP address
       Trusted Microsoft services

    Enabled Soft Delete
       Soft delete for blobs → 7 days
       Soft delete for containers → 7 days

    Future planned security tasks:
        Private Endpoints
        Managed Identities
        Firewall hardening
        Versioning

📅 Next Steps (Planned Work)

🔜 Automate:
    Move bronze data → cool tier after 30 days
    Delete bronze after 90 days

🔜 4. Ingest F1 2024 Data into Bronze

    Data sources:
        Openf1 API

    FastF1 Python library

🔜 5. Begin Silver + Gold transformations

    Using Databricks or Azure Data Factory.

🏁 Conclusion

    So far, I have successfully:
    Designed the foundational Azure infrastructure
    Implemented secure, industry-standard storage architecture
    Set up core identity, access, and security configurations
    Prepared the data lake for ingestion of F1 datasets
    This progress forms the backbone of the full F1 2024 Data Engineering Pipeline that I will build in future phases.
