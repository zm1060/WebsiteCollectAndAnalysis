import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load JSON data from file
with open('certificate_results_custom.json', 'r', encoding='utf-8') as file:
    certificates = json.load(file)

# Filter out certificates with empty issuer and subject
certificates = [cert for cert in certificates if cert.get('issuer') and cert.get('subject')]

# Convert to DataFrame
df = pd.DataFrame(certificates)

# Total number of certificates
total_certificates = len(df)

# Analyze different issuer counts
issuer_counts = df['issuer'].value_counts()

# Analyze certificate validity period distribution
df['notBefore'] = pd.to_datetime(df['notBefore'])
df['notAfter'] = pd.to_datetime(df['notAfter'])
df['validity_days'] = (df['notAfter'] - df['notBefore']).dt.days

# Plot validity period distribution
plt.figure(figsize=(10, 6))
plt.hist(df['validity_days'], bins=30, color='blue', edgecolor='black')
plt.title('Certificate Validity Period Distribution')
plt.xlabel('Validity Period (days)')
plt.ylabel('Number of Certificates')
plt.savefig('validity_distribution.png', dpi=500)
plt.show()

# Print statistical results
print(f"Total Certificates: {total_certificates}")
print("\nIssuer-wise Certificate Counts:")
print(issuer_counts)
self_signed_count = df['isSelfSigned'].sum()
print(f"Self-signed Certificates: {self_signed_count}")
expired_count = df['isExpired'].sum()
print(f"Expired Certificates: {expired_count}")
df['sans_count'] = df['sans'].apply(len)
print(f"Average SANs per Certificate: {df['sans_count'].mean()}")
print(f"Maximum SANs per Certificate: {df['sans_count'].max()}")

# Analyze issuer country information
df['issuer_country'] = df['issuer'].apply(lambda x: x.get('countryName', 'Unknown'))
issuer_country_counts = df['issuer_country'].value_counts()

# Analyze subject country information
df['subject_country'] = df['subject'].apply(lambda x: x.get('countryName', 'Unknown'))
subject_country_counts = df['subject_country'].value_counts()

mismatched_count = df['isMismatched'].sum()

# Analyze issuer and subject organizationName information
df['issuer_organization'] = df['issuer'].apply(lambda x: x.get('organizationName', 'Unknown'))
df['subject_organization'] = df['subject'].apply(lambda x: x.get('organizationName', 'Unknown'))
issuer_organization_counts = df['issuer_organization'].value_counts()
subject_organization_counts = df['subject_organization'].value_counts()

# Print statistical results
print("\nIssuer-wise OrganizationName Counts:")
print(issuer_organization_counts)
print("\nSubject-wise OrganizationName Counts:")
print(subject_organization_counts)

# New Distribution Plots
fields_to_analyze = ['issuer', 'subject', 'issuer_country', 'subject_country', 'issuer_organization', 'subject_organization']

for field in fields_to_analyze:
    plt.figure(figsize=(10, 6))
    field_counts = df[field].value_counts().head(20)
    field_counts.plot(kind='bar', color='teal', edgecolor='black')
    plt.title(f'Distribution of {field.title().replace("_", " ")}')
    plt.xlabel(field.title().replace("_", " "))
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{field}_distribution.png')
    plt.show()
