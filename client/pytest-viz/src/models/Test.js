function makeCollectedTestLeaf(test){
    return {
        name: test.name,
        file: false,
        singleTest: true,
        testRan: false,
        id: test.nodeId
    }
}


function makeExecutedTestLeaf(test){
    return {
        name: test.name,
        file: false,
        singleTest: true,
        testRan: true,
        passed: test.passed,
        id: test.nodeId,
        errorRepr: test.errorLog
      }
}

function makeTestTree(testsResponse, makeLeafFunction) {
    var tree = [];
    const directories = Object.entries(testsResponse.tests);

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


export default {
  convertResponseToCollectedTestsTree(response) {
    return makeTestTree(response.data, makeCollectedTestLeaf);
  },
  convertResponseToExecutedTestsTree(response) {
    return makeTestTree(response.data, makeExecutedTestLeaf);
  },
  filterOutTestModules(allSelections){
      return allSelections.filter((selection) => {
          return selection.singleTest;
      })
  }
}
