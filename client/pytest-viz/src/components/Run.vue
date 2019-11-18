<template>
  <v-content>
    <v-container class="fill-height" justify="center">
      <v-card class="mx-auto" raised>
        <v-toolbar color="teal" dark>
          <v-toolbar-title>Tests</v-toolbar-title>
        </v-toolbar>
        <div class="text-center">
          <v-btn class="ma-2" tile color="orange" light @click="collectTests()">Collect</v-btn>
          <template v-if="nothingSelected(selection)">
              <v-btn class="ma-2" tile color="green" @click="RunAllTests()">Run All</v-btn>
          </template>
          <template v-else>
              <v-btn class="ma-2" tile color="green" @click="RunSelectedTests()">Run Selected</v-btn>
          </template>
          
        </div>
        <v-treeview
          v-model="selection"
          :items="tests"
          selectable
          item-key="id"
          open-on-click
          return-object
        >
          <template v-slot:prepend="{ item, open }">
            <v-icon v-if="item.file">
              {{ open ? 'mdi-folder-open' : 'mdi-folder' }}
            </v-icon>
            <v-icon color="green" v-else-if="item.testRan && item.passed">
              {{ 'mdi-flash' }}
            </v-icon>
            <v-icon color="red" v-else-if="item.testRan && !item.passed">
              {{ 'mdi-flash' }}
            </v-icon>
            <v-icon v-else>
              {{ 'mdi-flash-outline' }}
            </v-icon>
          </template>
        </v-treeview>
      </v-card>
    </v-container>
  </v-content>
</template>
  <!-- <v-row align="center">
    <v-card class="mx-auto" raised>
      <v-toolbar color="teal" dark>
        <v-toolbar-title>Tests</v-toolbar-title>
      </v-toolbar>

      <v-row align="center">
        <div class="my-2">
          <v-btn color="orange" @click="collectTests()">Collect</v-btn>
        </div>
        <div class="my-2">
          <v-btn color="lime" @click="RunAllTests()">Run All</v-btn>
        </div>
      </v-row>

      <v-list subheader>
        <v-list-item-group v-model="tests" color="primary">
          <span v-for="(item, i) in tests" :key="i">
            <v-subheader>{{i}}</v-subheader>
            <span v-for="(test, j) in item" :key="j">
              <v-row justify="space-between">
                <v-list-item @click="runOneTest(test.nodeId)">
                  <v-list-item-content>
                    <v-col cols="auto">
                      <v-icon v-if="test.passed === undefined">mdi-checkbox-blank-outline</v-icon>
                      <v-icon v-else-if="test.passed === true" color="green">mdi-thumb-up</v-icon>
                      <v-icon v-else color="red">mdi-thumb-down</v-icon>
                      {{test.name}}
                    </v-col>
                  </v-list-item-content>
                </v-list-item>
              </v-row>
            </span>
          </span>
        </v-list-item-group>
      </v-list>
    </v-card>

  </v-row> -->

<script>
import ApiService from "@/services/ApiService";
import Test from "@/models/Test";

export default {
  name: "Run",

  data: () => ({
    tests: [],
    selection: []
  }),

  // async mounted() {
  //   const resp = await ApiService.collectTests();
  //   this.tests = resp.data.tests;
  // },

  methods: {
    async collectTests () {
      const resp = await ApiService.collectTests();
      this.tests = Test.convertResponseToCollectedTestsTree(resp);
    },
    async RunAllTests () {
      const resp = await ApiService.runTests();
      this.tests = Test.convertResponseToExecutedTestsTree(resp);
    },
    async RunSelectedTests () {
      const selectedTests = Test.filterOutTestModules(this.selection);
      console.log(selectedTests);
      const resp = await ApiService.RunSelectedTests(selectedTests);
      this.tests = Test.convertResponseToExecutedTestsTree(resp);
    },
    nothingSelected (selection) {
        const selectedTests = Test.filterOutTestModules(selection);
        return selectedTests.length < 1;
    }
  }
};
</script>
