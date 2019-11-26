import ApiService from "@/services/ApiService";

function  convertResponseToCollectedTestsTree(response) {
  return response.data.collectedTestsTree;
}

function convertResponseToExecutedTestsTree(response) {
  return response.data.executedTestsTree;
}

function findFailedTests(allExecutedTests){
  if (!allExecutedTests[0].children[0].passed){  // TODO: finds only 1
    return [allExecutedTests[0].children[0]] ;
  }
}

function getTestCasesOnly(allSelections){
  return allSelections.filter((selection) => {
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
    this.vueComponent.collected_tests = convertResponseToCollectedTestsTree(resp);
  }
  async runAllTests(){
    this.vueComponent.testExecutionInProgress = true;
    const resp = await ApiService.runTests();
    this.vueComponent.testExecutionInProgress = false;
    this.processTestExecutionResponse(resp);
    this.vueComponent.collected_tests = convertResponseToCollectedTestsTree(resp);
  }
  async runSelectedTests(){
    const selectedTests = getTestCasesOnly(this.vueComponent.selection);
    this.vueComponent.testExecutionInProgress = true;
    const resp = await ApiService.RunSelectedTests(selectedTests);
    this.vueComponent.testExecutionInProgress = false;
    if (resp.data.error){
      this.collectTests();
      this.vueComponent.executed_tests = [];
    }
    else{
      this.processTestExecutionResponse(resp);
    }
  }
  processTestExecutionResponse (resp) {
    let executedTests = convertResponseToExecutedTestsTree(resp);
    this.vueComponent.executed_tests = executedTests;
    this.vueComponent.failedTests = findFailedTests(executedTests);
  }
}

export default {
  Synchronizer,
  getTestCasesOnly(allSelections){
      return getTestCasesOnly(allSelections);
  },
}
