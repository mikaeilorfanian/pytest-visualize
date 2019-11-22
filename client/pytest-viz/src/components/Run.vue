<template>

  <v-container>
    <v-toolbar color="teal" dark>
      <v-toolbar-title>Tests</v-toolbar-title>
      <div class="text-center">
        <v-btn class="ma-2" tile color="orange" light @click="collectTests()">Collect</v-btn>
        <template v-if="nothingSelected(selection)">
            <v-btn class="ma-2" tile color="green" @click="RunAllTests()">Run All</v-btn>
        </template>
        <template v-else>
            <v-btn class="ma-2" tile color="green" @click="RunSelectedTests()">Run Selected</v-btn>
        </template>
      </div>
    </v-toolbar>

    <v-row>
      <v-col>
        <v-treeview
          v-model="selection"
          :items="collected_tests"
          item-key="id"
          selectable
          return-object
          open-on-click
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
      </v-col>

      <v-divider vertical></v-divider>

      <v-col class="pa-6" cols="6">
        <template v-if="!executed_tests.length">
          Run some tests to see the results here!
        </template>
        <template v-else>
          <v-treeview
            open-all
            :items="executed_tests"
            item-key="id"
            open-on-click
            activatable
            :active="active"
            return-object
            @update:active="showError"
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
            <!-- {{ node.name }} -->
        </template>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">Error details</span>
        </v-card-title>
        <v-card-text v-model="error"><pre>{{error}}</pre></v-card-text>
      </v-card>
    </v-dialog>
  </v-container>

</template>

<script>
import ApiService from "@/services/ApiService";
import Test from "@/models/Test";

export default {
  name: "Run",

  data: () => ({
    collected_tests: [],
    selection: [],
    executed_tests: [],
    active: [],
    dialog: false,
    error: null
  }),

  // async mounted() {
  //   const resp = await ApiService.collectTests();
  //   this.tests = resp.data.tests;
  // },

  methods: {
    async collectTests () {
      const resp = await ApiService.collectTests();
      this.collected_tests = Test.convertResponseToCollectedTestsTree(resp);
    },
    async RunAllTests () {
      const resp = await ApiService.runTests();
      this.executed_tests = Test.convertResponseToExecutedTestsTree(resp);
    },
    async RunSelectedTests () {
      const selectedTests = Test.filterOutTestModules(this.selection);
      const resp = await ApiService.RunSelectedTests(selectedTests);
      this.executed_tests = Test.convertResponseToExecutedTestsTree(resp);
    },
    nothingSelected (selection) {
        const selectedTests = Test.filterOutTestModules(selection);
        return selectedTests.length < 1;
    },
    showError (selected) {
      if (selected.length) {
        console.log(selected);
        console.log(selected[0].errorRepr);
        this.error = selected[0].errorRepr;
        this.dialog = true;
      }
      
    }
  },

  sockets: {
        connect: function () {
            console.log('socket connected');
            if (this.nothingSelected(this.selection)) {
              this.collectTests();
              this.selection = this.collected_tests;
              this.RunAllTests();
            }
            else {
              this.RunSelectedTests();
            }
        },
        // customEmit: function (data) {
        //     console.log('this method was fired by the socket server. eg: io.emit("customEmit", data)')
        // }
    },
    // methods: {
    //     clickButton: function (data) {
    //         // $socket is socket.io-client instance
    //         this.$socket.emit('emit_method', data)
    //     }
    // }
};
</script>
