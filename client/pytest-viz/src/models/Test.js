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

function getTestCasesOnly(allSelectedTests){  // TODO rename this function to getTestCasesFromTree
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
      vueComponent.executedTests = [];
      vueComponent.failedTests = [];
    }
    else{
      vueComponent.userCodeFailure = null;
      vueComponent.collectedTests = getCollectedTestsTree(resp);
    }
  }
  async runAllTests(vueComponent){
    vueComponent.testExecutionInProgress = true;
    const resp = await ApiService.runTests();
    vueComponent.testExecutionInProgress = false; // TODO handle user code error here also
    this.processTestExecutionResponse(resp, vueComponent);
    vueComponent.collectedTests = getCollectedTestsTree(resp);
  }
  async runSelectedTests(vueComponent){
    const selectedTests = getTestCasesOnly(vueComponent.selection);
    vueComponent.testExecutionInProgress = true;
    const resp = await ApiService.runSelectedTests(selectedTests);
    vueComponent.testExecutionInProgress = false;
    if (resp.data.error){
        if (resp.data.error.code == 1001){
            vueComponent.userCodeFailure = resp.data.error.message;
            vueComponent.collectedTests = [];
            vueComponent.executedTests = [];
            vueComponent.failedTests = [];
        }
        else{
            this.collectTests(vueComponent);
            vueComponent.executedTests = [];
        }
    }
    else{
      this.processTestExecutionResponse(resp, vueComponent);
    }
  }
  processTestExecutionResponse (resp, vueComponent) {
    let executedTests = getExecutedTestsTree(resp);
    vueComponent.executedTests = executedTests;
    vueComponent.failedTests = findFailedTests(executedTests);
    vueComponent.userCodeFailure = null;
  }
}

export default {
  Synchronizer,
  getTestCasesOnly(allSelectedTests){
      return getTestCasesOnly(allSelectedTests);
  },
}
