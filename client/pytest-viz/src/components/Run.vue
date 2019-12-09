<template>

  <v-container>
    <v-toolbar color="teal" dark>
      <v-toolbar-title>Available Tests</v-toolbar-title>
      <div class="text-center">
        <v-btn class="ma-2" tile color="orange" light @click="collectTests()">Collect</v-btn>
        <template v-if="nothingSelected(selection)">
            <v-btn class="ma-2" tile color="green" @click="runAllTests()">Run All</v-btn>
        </template>
        <template v-else>
            <v-btn class="ma-2" tile color="green" @click="runSelectedTests()">Run Selected</v-btn>
        </template>
      </div>
    </v-toolbar>

    <v-row>
      <v-col class="pa-6">
        <template v-if="testCollectionInProgress">
          <div class="text-center">
            <v-progress-circular
              :size="70"
              :width="7"
              color="orange"
              indeterminate
            ></v-progress-circular>
          </div>
        </template>
        <template v-if="!collectedTests.length">
          Collect tests to see them here!
        </template>
        <template v-else>
          <v-treeview
            v-model="selection"
            :items="collectedTests"
            item-key="id"
            selectable
            return-object
            open-on-click
          >
            <template v-slot:prepend="{ item, open }">
              <v-icon v-if="item.isPackage">
                {{ open ? 'mdi-folder-open' : 'mdi-folder' }}
              </v-icon>
              <v-icon v-else-if="item.isModule">
                {{ 'mdi-language-python' }}
              </v-icon>
              <v-icon v-else-if="item.isKlass">
                {{ 'mdi-file-table-box-multiple-outline' }}
              </v-icon>
              <v-icon v-else>
                {{ 'mdi-flash-outline' }}
              </v-icon>
            </template>
          </v-treeview>
        </template>
      </v-col>

      <v-divider vertical></v-divider>

      <v-col class="pa-6" cols="6">
        <template v-if="testExecutionInProgress">
          <div class="text-center">
            <v-progress-circular
              :size="70"
              :width="7"
              color="green"
              indeterminate
            ></v-progress-circular>
          </div>
        </template>
        <template v-if="!executedTests.length">
          Run some tests to see the results here!
        </template>
        <template v-else>
          <v-treeview
            :items="executedTests"
            item-key="id"
            activatable
            :active="active"
            return-object
            @update:active="showErrorDialog"
            :open.sync="open"
            open-on-click
            open-all
          >
            <template v-slot:prepend="{ item, open }">
              <v-icon v-if="item.isPackage">
                {{ open ? 'mdi-folder-open' : 'mdi-folder' }}
              </v-icon>
              <v-icon v-else-if="item.isModule">
                {{ 'mdi-language-python' }}
              </v-icon>
              <v-icon v-else-if="item.isKlass">
                {{ 'mdi-file-table-box-multiple-outline' }}
              </v-icon>
              <v-icon color="green" v-else-if="item.wasExecuted && item.passed">
                {{ 'mdi-flash' }}
              </v-icon>
              <v-icon color="red" v-else>
                {{ 'mdi-flash' }}
              </v-icon>
            </template>
          </v-treeview>
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

    <v-sheet 
      color="black lighten-2" 
      v-model="panel"
      v-for="(test) in failedTests"
      :key="test.id"
      dark
      >
      <pre>{{test.errorRepr}}</pre>
    </v-sheet>

    <template  v-if="userCodeFailure">
      <v-sheet :elevation=12 dark color="red">Test collection failed!</v-sheet>
        <v-divider></v-divider>
      <v-sheet 
        color="black lighten-2" 
        dark
        >
        <pre>{{userCodeFailure}}</pre>
      </v-sheet>
    </template>
  </v-container>

</template>

<script>
import ApiService from "@/services/ApiService";
import Test from "@/models/Test";

let syncer = new Test.Synchronizer();

export default {
  name: "Run",

  data: () => ({
    collectedTests: [],
    selection: [],
    executedTests: [],
    active: [],
    dialog: false,
    error: null,
    panel: 0,  // always open the first panel only
    failedTests: [],
    testExecutionInProgress: false,
    testCollectionInProgress: false,
    userCodeFailure: null,
    open: []
  }),

  methods: {
    async collectTests () {
      syncer.collectTests(this);
    },
    async runAllTests () {
      syncer.runAllTests(this);
    },
    async runSelectedTests () {
      syncer.runSelectedTests(this);
    },
    nothingSelected (selection) {
        const selectedTests = Test.getTestCasesOnly(selection);
        return selectedTests.length < 1;
    },
    showErrorDialog (selected) {
      if (selected.length) {
        this.error = selected[0].errorRepr;
        this.dialog = true;
      }
      
    }
  },

  sockets: {
    connect: function () {
        console.log('socket connected to backend');
        if (this.nothingSelected(this.selection)) {
        }
        else {
          // this.runSelectedTests();
        }
    },
  },
};
</script>
