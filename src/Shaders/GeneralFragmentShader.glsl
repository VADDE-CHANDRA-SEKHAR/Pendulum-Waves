#version 460 core

struct Material {
	vec4 color;
	float ambientCoefficient;
	float diffuseCoefficient;
	float specularCoefficient;
	float shininess;
};

struct Light {
	vec3 position;
	vec3 color;
};

in Attributes {
	vec3 fragPosition;
	vec3 normal;
} inAttributes;

uniform bool lightened;
uniform vec3 eyePosition;
uniform Light light;
uniform Material material;

float attenuation(in Light light) 
{
	float distance = length(light.position - inAttributes.fragPosition);
	float attenuation = 1.f / (1.f + 0.024f * distance * 0.0021f * distance * distance);
	return attenuation;
}

vec3 calculatePointLight(in vec3 colorAmbient, in vec3 colorDiffuse, in vec3 colorSpecular, in vec3 eyeDirection) 
{
	// ambient
	vec3 ambientComponent = colorAmbient; 

	// diffuse
	vec3 lightDirection = normalize(light.position - inAttributes.fragPosition);
	float lightAngle = dot(lightDirection, inAttributes.normal);
	lightAngle = max(lightAngle, 0.0);
	vec3 diffuseComponent = colorDiffuse.rgb * light.color * lightAngle;

	// specular
	// vec3 reflectedLight = reflect(-lightDirection, inAttributes.normal);
	vec3 halfwayVector = normalize(lightDirection + eyeDirection);
	float eyeAngle = pow(max(dot(halfwayVector, inAttributes.normal), 0.0), material.shininess);
	vec3 specularComponent = colorSpecular * light.color * eyeAngle;
		
	vec3 result = ambientComponent + ((diffuseComponent + specularComponent) * attenuation(light));

	return result;
}


void main() 
{
	if (!lightened)
	{
		gl_FragColor = material.color;	
		return;
	}

	vec3 colorAmbient = material.color.rgb * material.ambientCoefficient;
	vec3 colorDiffuse = material.color.rgb * material.diffuseCoefficient;
	vec3 colorSpecular = material.color.rgb * material.specularCoefficient;
	float alpha = material.color.a;

	vec3 eyeDirection = normalize(eyePosition - inAttributes.fragPosition);
	gl_FragColor = vec4(calculatePointLight(colorAmbient, colorDiffuse, colorSpecular, eyeDirection), alpha);
}