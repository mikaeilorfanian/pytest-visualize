import ApiService from "@/services/ApiService";

function  getCollectedTestsTree(response) {
  return response.data.collectedTestsTree;
}

function getExecutedTestsTree(response) {
  return response.data.executedTestsTree;
}

function findFailedTests(allExecutedTests){
  const firstTest = allExecutedTests[0].children[0];
  if (!firstTest.passed){  // TODO: finds only 1
    return [firstTest] ;
  }
}

function getTestCasesOnly(allSelectedTests){
  return allSelectedTests.filter((selection) => {
      return selection.isSingleTest;
  })
}

class Synchronizer {
  async collectTests(vueComponent){
    vueComponent.testCollectionInProgress = true;
    const resp = await ApiService.collectTests();
    vueComponent.testCollectionInProgress = false;
    if (resp.data.error){
      vueComponent.userCodeFailure = resp.data.error.message;
      vueComponent.collectedTests = [];
    }
    else{
      vueComponent.userCodeFailure = null;
      vueComponent.collectedTests = getCollectedTestsTree(resp);
    }
  }
  async runAllTests(vueComponent){
    vueComponent.testExecutionInProgress = true;
    const resp = await ApiService.runTests();
    vueComponent.testExecutionInProgress = false;
    this.processTestExecutionResponse(resp, vueComponent);
    vueComponent.collectedTests = getCollectedTestsTree(resp);
  }
  async runSelectedTests(vueComponent){
    const selectedTests = getTestCasesOnly(vueComponent.selection);
    vueComponent.testExecutionInProgress = true;
    const resp = await ApiService.runSelectedTests(selectedTests);
    vueComponent.testExecutionInProgress = false;
    if (resp.data.error){
      this.collectTests(vueComponent);
      vueComponent.executedTests = [];
    }
    else{
      this.processTestExecutionResponse(resp, vueComponent);
    }
  }
  processTestExecutionResponse (resp, vueComponent) {
    let executedTests = getExecutedTestsTree(resp);
    vueComponent.executedTests = executedTests;
    vueComponent.failedTests = findFailedTests(executedTests);
  }
}

export default {
  Synchronizer,
  getTestCasesOnly(allSelectedTests){
      return getTestCasesOnly(allSelectedTests);
  },
}
