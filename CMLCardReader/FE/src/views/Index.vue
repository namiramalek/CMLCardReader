<template>
  <div style="height: 100vh; overflow-y: auto">
    <v-container
      class="white px-4 px-md-16 py-5 pb-16"
      style="min-height: 100%"
    >
      <v-dialog v-model="errorDialog" width="32rem">
        <v-sheet class="pa-4">
          <h2 class="mb-4">Error getting cards</h2>
          <p class="grey--text text--darken-2">
            There was an error getting the cards. Please refresh the page and
            try again.
          </p>
          <v-btn color="primary" rounded class="py-6" @click="retry()">
            Retry
          </v-btn>
        </v-sheet>
      </v-dialog>
      <h1>All business cards</h1>

      <form class="my-4" @submit.prevent="search()">
        <div class="d-flex">
          <v-text-field
            style="border-radius: 0; border-right: none"
            outlined
            dense
            label="Search business cards"
            v-model="keyword"
          />
          <v-btn
            style="height: 40px"
            type="submit"
            color="primary"
            elevation="0"
            >Search</v-btn
          >
        </div>
        <v-btn @click="reset()" v-if="filteredBusinessCards">
          Reset filters
        </v-btn>
      </form>

      <h4
        v-if="!!businessCards"
        class="grey--text text--darken-2 font-weight-medium mb-4"
      >
        Showing
        {{
          filteredBusinessCards
            ? filteredBusinessCards.length
            : businessCards.length
        }}
        cards
      </h4>
      <div v-if="businessCards">
        <div
          v-if="businessCards.length === 0"
          class="pa-8 blue-grey lighten-5 d-flex align-center"
        >
          <h3>No business cards yet</h3>
        </div>
        <div
          v-if="filteredBusinessCards?.length === 0"
          class="pa-8 blue-grey lighten-5 d-flex align-center"
        >
          <h3>No business cards match the criteria.</h3>
        </div>
        <business-card-table
          @delete="deleteBusinesscard($event)"
          :businessCards="
            filteredBusinessCards ? filteredBusinessCards : businessCards
          "
          v-else
        />
      </div>
      <div v-else class="pa-8 blue-grey lighten-5 d-flex align-center">
        <v-progress-circular
          indeterminate
          color="primary"
          size="32"
          width="2"
          class="mr-4"
        ></v-progress-circular>
        <h3>Getting business cards</h3>
      </div>
    </v-container>
  </div>
</template>

<script>
import BusinessCardTable from "../components/BusinessCardTable.vue";
export default {
  name: "Index",
  components: {
    BusinessCardTable,
  },
  data() {
    return {
      errorDialog: false,
      businessCards: null,
      filteredBusinessCards: null,
      keyword: "",
    };
  },
  created() {
    this.$http
      .get("/")
      .then(({ data }) => {
        this.businessCards = data;
        console.log(data);
      })
      .catch(() => {
        this.errorDialog = true;
      });
  },
  methods: {
    retry() {
      window.location.reload();
    },
    deleteBusinesscard(id) {
      this.$http
        .delete(`/business-card/${id}`)
        .then(() => {
          alert("Business card deleted");
          this.businessCards = this.businessCards.filter(
            (card) => card.id.S !== id
          );
        })
        .catch(() => {
          alert("Something went wrong, please try again");
        });
    },
    search() {
      this.filteredBusinessCards = this.businessCards.filter((card) => {
        const entities = JSON.stringify(card.entities).toLowerCase();
        return entities.includes(this.keyword);
      });
    },
    reset() {
      this.keyword = null;
      this.filteredBusinessCards = null;
    },
  },
};
</script>