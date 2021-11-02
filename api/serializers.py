from rest_framework import serializers

from .models import PackageRelease, Project
from .pypi import version_exists, latest_version, project_name


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageRelease
        fields = ["name", "version"]
        extra_kwargs = {"version": {"required": False}}

    def validate(self, data):

    #    if package_name in data:
    #        raise serializers.ValidationError({"error": "Project name already exists"})
    #    else:
    #        pass

        found = False
        for i in data:
            if i == 'version':
                package_version = data[i]
                found = True

        if found:
            v_exist = version_exists(data["name"], package_version)
            if v_exist:
                return data
            else:
                raise serializers.ValidationError({"error": "One or more packages doesn't exist"})
        
        else:
            last = latest_version(data["name"])
            if last == None:
                raise serializers.ValidationError({"error": "One or more packages doesn't exist"})
            else:
                data['version'] = last
                return data
        
        return data

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "packages"]

    packages = PackageSerializer(many=True)

    def create(self, validated_data):
        
        packages = validated_data["packages"]
        projeto = Project.objects.create(name=validated_data["name"])
        
        length_pack = len(packages)
        i = 0
        while i < length_pack:
            package = PackageRelease.objects.create(name=packages[i]['name'], version=packages[i]['version'], project=projeto)
            i += 1
        
        projeto.save()
        return projeto
