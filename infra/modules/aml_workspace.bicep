param location string
param workspaceName string
param storageAccountName string
param keyVaultName string
param acrName string

resource workspace 'Microsoft.MachineLearningServices/workspaces@2024-04-01' = {
  name: workspaceName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: workspaceName
    description: 'BankCore MLOps Azure Machine Learning workspace'

    storageAccount: resourceId(
      'Microsoft.Storage/storageAccounts',
      storageAccountName
    )

    keyVault: resourceId(
      'Microsoft.KeyVault/vaults',
      keyVaultName
    )

    containerRegistry: resourceId(
      'Microsoft.ContainerRegistry/registries',
      acrName
    )
  }
}

output workspaceName string = workspace.name