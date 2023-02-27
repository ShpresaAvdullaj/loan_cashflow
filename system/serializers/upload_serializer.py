# from system.tasks import populate_database
# from django.core.files.storage import FileSystemStorage
# from django.core.files import File
# from rest_framework import serializers
#
#
# class UploadSerializer(serializers.Serializer):
#     loan_file = serializers.FileField(max_length=100, allow_empty_file=False)
#     cashflow_file = serializers.FileField(max_length=100, allow_empty_file=False)
#
#     class Meta:
#         fields = ["loan_file", "cashflow_file", ]
#
#     def create(self, validated_data):
#         loan_file = self.context["loan_file"]
#         cashflow_file = self.context["cashflow_file"]
#
#         storage = FileSystemStorage()
#         storage.save(loan_file.name, File(loan_file))
#         storage.save(cashflow_file.name, File(cashflow_file))
#         return populate_database.delay(
#             path_loan=storage.path(loan_file.name), path_cashflow=storage.path(cashflow_file.name))
