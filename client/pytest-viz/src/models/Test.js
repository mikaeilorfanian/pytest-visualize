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
  constructor(vueComponent){
    this.vueComponent = vueComponent;
  }
  async collectTests(){
    this.vueComponent.testCollectionInProgress = true;
    const resp = await ApiService.collectTests();
    this.vueComponent.testCollectionInProgress = false;
    this.vueComponent.collectedTests = getCollectedTestsTree(resp);
  }
  async runAllTests(){
    this.vueComponent.testExecutionInProgress = true;
    const resp = await ApiService.runTests();
    this.vueComponent.testExecutionInProgress = false;
    this.processTestExecutionResponse(resp);
    this.vueComponent.collectedTests = getCollectedTestsTree(resp);
  }
  async runSelectedTests(){
    const selectedTests = getTestCasesOnly(this.vueComponent.selection);
    this.vueComponent.testExecutionInProgress = true;
    const resp = await ApiService.runSelectedTests(selectedTests);
    this.vueComponent.testExecutionInProgress = false;
    if (resp.data.error){
      this.collectTests();
      this.vueComponent.executedTests = [];
    }
    else{
      this.processTestExecutionResponse(resp);
    }
  }
  processTestExecutionResponse (resp) {
    let executedTests = getExecutedTestsTree(resp);
    this.vueComponent.executedTests = executedTests;
    this.vueComponent.failedTests = findFailedTests(executedTests);
  }
}

export default {
  Synchronizer,
  getTestCasesOnly(allSelectedTests){
      return getTestCasesOnly(allSelectedTests);
  },
}
