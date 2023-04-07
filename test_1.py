from sensor.entity.artifact_entity import DataValidationArtifact
x = DataValidationArtifact(report_file_path="/home/honey/Desktop/try/1/sensor_fault/artifact/03202023__130633/data_validation/report.yaml")

print("*************************")
print(x)
print("*************************")
y = x.__dict__
print(y)
print("*************************")
z=DataValidationArtifact(y)
print(z)
print("*************************")
z=DataValidationArtifact(**y)
print(z)
