import ApiService from "@/services/ApiService";

function  getCollectedTestsTree(response) {
  return response.data.collectedTestsTree;
}

function getExecutedTestsTree(response) {
  return response.data.executedTestsTree;
}

function getTestCasesOnly(allSelectedTests){  // TODO rename this function to getSelectedTestsFromTree
  return allSelectedTests.filter((selection) => {
      return selection.isSingleTest;
  })
}

class Synchronizer {
  userCodeNotCompiling(response, vueComponent){
    vueComponent.userCodeFailure = response.data.error.message;
    vueComponent.collectedTests = [];
    vueComponent.executedTests = [];
    // vueComponent.failedTests = [];
  }
  userCodeUpdated(vueComponent){
    this.collectTests(vueComponent);
    vueComponent.executedTests = [];
    vueComponent.alert = true;
  }
  handleError(response, vueComponent){
    if (response.data.error.code == 1001){
      this.userCodeNotCompiling(response, vueComponent);
    }
    else{  // user code was updated and led to inconsistent state 
      this.userCodeUpdated(vueComponent);
    }
  }
  async collectTests(vueComponent){
    vueComponent.testCollectionInProgress = true;
    const resp = await ApiService.collectTests();
    vueComponent.testCollectionInProgress = false;
    if (resp.data.error){
      this.handleError(resp, vueComponent);
      vueComponent.collectedTestsCount = null;
    }
    else{
      vueComponent.userCodeFailure = null;
      vueComponent.collectedTests = getCollectedTestsTree(resp);
      vueComponent.collectedTestsCount = resp.data.collectedTestsCount;
      vueComponent.alert = null;
    }
  }
  async runAllTests(vueComponent){
    vueComponent.testExecutionInProgress = true;
    const resp = await ApiService.runTests();
    vueComponent.testExecutionInProgress = false;
    if (resp.data.error){
      this.handleError(resp, vueComponent);
      vueComponent.executedTestsCount = null;
    }
    else{
      this.processTestExecutionResponse(resp, vueComponent);
      vueComponent.collectedTests = getCollectedTestsTree(resp);
    }
  }
  async runSelectedTests(vueComponent){
    const selectedTests = getTestCasesOnly(vueComponent.selection);
    vueComponent.testExecutionInProgress = true;
    const resp = await ApiService.runSelectedTests(selectedTests);
    vueComponent.testExecutionInProgress = false;
    if (resp.data.error){
      this.handleError(resp, vueComponent);
      vueComponent.executedTestsCount = null;
    }
    else{
      this.processTestExecutionResponse(resp, vueComponent);
    }
  }
  async runFailedTests(vueComponent){
    vueComponent.selection = vueComponent.failedTests;
    await this.runSelectedTests(vueComponent);
  }
  processTestExecutionResponse (resp, vueComponent) {
    let executedTests = getExecutedTestsTree(resp);
    vueComponent.executedTests = executedTests;
    vueComponent.failedTests = resp.data.failedTests;
    vueComponent.userCodeFailure = null;
    vueComponent.executedTestsCount = resp.data.executedTestsCount;
    vueComponent.alert = null;
  }
  async runTestsInPaths(vueComponent){
    vueComponent.testExecutionInProgress = true;
    const resp = await ApiService.runTestsForPaths(vueComponent.selection);
    vueComponent.testExecutionInProgress = false;
    if (resp.data.error){
      this.handleError(resp, vueComponent);
      vueComponent.executedTestsCount = null;
    }
    else{
      this.processTestExecutionResponse(resp, vueComponent);
    }
  }
  async collectPaths(vueComponent){
    vueComponent.testCollectionInProgress = true;
    const resp = await ApiService.collectTestsPaths();
    vueComponent.testCollectionInProgress = false;
    if (resp.data.error){
      this.handleError(resp, vueComponent);
      vueComponent.collectedTestsCount = null;
    }
    else{
      vueComponent.userCodeFailure = null;
      vueComponent.collectedPaths = getCollectedTestsTree(resp);
      vueComponent.collectedTestsCount = resp.data.collectedPathsCount;
      vueComponent.alert = null;
    }
  }
  resetCollectedPaths(vueComponent) {
    vueComponent.collectedPaths = [];
    vueComponent.collectedTestsCount = null;
  }
}

export default {
  Synchronizer,
  getTestCasesOnly(allSelectedTests){
      return getTestCasesOnly(allSelectedTests);
  },
}
