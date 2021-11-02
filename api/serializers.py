from rest_framework import serializers

from .models import PackageRelease, Project
from .pypi import version_exists, latest_version


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageRelease
        fields = ["name", "version"]
        extra_kwargs = {"version": {"required": False}}

    def validate(self, data):

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
        proj_new = Project.objects.create(name=validated_data["name"])
        
        dic_pack = {}
        length_pack = len(packages)
        i = 0
        while i < length_pack:
            if (packages[i]['name'], packages[i]['version']) in dic_pack.items():
                proj_new.delete()
                raise serializers.ValidationError({"Error:""project name already exists"})
            else:
                package = PackageRelease.objects.create(name=packages[i]['name'], version=packages[i]['version'], project=proj_new)
                dic_pack[packages[i]['name']] = packages[i]['version']
                i += 1
        
        proj_new.save()
        return proj_new
