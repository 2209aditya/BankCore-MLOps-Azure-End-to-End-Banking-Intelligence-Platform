param location string
param clusterName string
param acrId string

resource aks 'Microsoft.ContainerService/managedClusters@2024-05-01' = {
  name: clusterName
  location: location

  identity: {
    type: 'SystemAssigned'
  }

  properties: {
    dnsPrefix: clusterName

    agentPoolProfiles: [
      {
        name: 'system'
        count: 2
        vmSize: 'Standard_D4s_v5'
        osType: 'Linux'
        mode: 'System'
        type: 'VirtualMachineScaleSets'
      }
    ]

    networkProfile: {
      networkPlugin: 'azure'
      loadBalancerSku: 'standard'
    }
  }
}

resource acrPull 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(
    aks.id,
    acrId,
    'AcrPull'
  )

  scope: resourceId(
    'Microsoft.ContainerRegistry/registries',
    last(split(acrId, '/'))
  )

  properties: {
    principalId: aks.identity.principalId
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '7f951dda-4ed3-4680-a7ca-43fe172d538d'
    )
    principalType: 'ServicePrincipal'
  }
}

output aksName string = aks.name