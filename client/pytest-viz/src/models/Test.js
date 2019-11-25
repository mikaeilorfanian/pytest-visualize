import ApiService from "@/services/ApiService";

function makeCollectedTestLeaf(test){
    return {
        name: test.name,
        file: false,
        singleTest: true,
        testRan: false,
        id: test.nodeId
    }
}

function makeTestTree(tests, makeLeafFunction) {
    var tree = [];
    const directories = Object.entries(tests);

    var i = 0;
    for (const [testModule, tests] of directories) {
        var children = [];
  
        for (const test of tests) {
          children.push(makeLeafFunction(test));
        }
  
        tree.push(
          {
            name: testModule,
            children: children,
            file: true,
            id: i
          }
        )
        i += 1;
      }
    return tree;
}

function  convertResponseToCollectedTestsTree(response) {
  return response.data.collectedTestsTree;
  return makeTestTree(response.data.collectedTets, makeCollectedTestLeaf);
}

function convertResponseToExecutedTestsTree(response) {
  return response.data.executedTestsTree;
}

function findFailedTests(allExecutedTests){
  if (!allExecutedTests[0].children[0].passed){  // TODO: finds only 1
    return [allExecutedTests[0].children[0]] ;
  }
}

function filterOutTestModules(allSelections){
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
    const selectedTests = filterOutTestModules(this.vueComponent.selection);
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
    // this.vueComponent.failedTests = findFailedTests(executedTests);
  }
}

export default {
  Synchronizer,
  filterOutTestModules(allSelections){
      return filterOutTestModules(allSelections);
  },
}
