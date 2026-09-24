param location string = resourceGroup().location

param prefix string = 'bankcore'

param storageAccountName string
param acrName string
param keyVaultName string
param amlWorkspaceName string
param aksName string
param openAIName string

module storage './modules/storage_adls.bicep' = {
  name: 'storage'
  params: {
    location: location
    storageAccountName: storageAccountName
    containerName: 'bankcore'
  }
}

module acr './modules/acr.bicep' = {
  name: 'acr'
  params: {
    location: location
    acrName: acrName
  }
}

module keyvault './modules/keyvault.bicep' = {
  name: 'keyvault'
  params: {
    location: location
    keyVaultName: keyVaultName
  }
}

module aml './modules/aml_workspace.bicep' = {
  name: 'aml'
  params: {
    location: location
    workspaceName: amlWorkspaceName
    storageAccountName: storage.outputs.storageAccountName
    keyVaultName: keyvault.outputs.keyVaultName
    acrName: acr.outputs.acrName
  }
}

module aks './modules/aks_cluster.bicep' = {
  name: 'aks'
  params: {
    location: location
    clusterName: aksName
    acrId: acr.outputs.acrId
  }
}

module openai './modules/openai.bicep' = {
  name: 'openai'
  params: {
    location: location
    accountName: openAIName
  }
}

module monitor './modules/monitor.bicep' = {
  name: 'monitor'
  params: {
    location: location
    prefix: prefix
  }
}