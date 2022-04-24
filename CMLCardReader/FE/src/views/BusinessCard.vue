<template>
  <div style="height: 100vh; overflow-y: auto">
    <v-container
      class="white"
      v-if="businessCard"
      style="padding-bottom: 128px"
    >
      <h1 class="mb-6">Business card details</h1>
      <div class="row">
        <div class="col-md-6">
          <img class="w-100" :src="businessCard.s3_url.S" alt="" />
          <v-btn width="200px" elevation="0" @click="readCard()">
            <span v-if="!isTtsLoading">
              <v-icon left> mdi-volume-high </v-icon>
              Read business card
            </span>
            <span v-else>
              <v-progress-circular
                :indeterminate="isTtsLoading"
                :size="16"
                :width="2"
              />
            </span>
          </v-btn>
        </div>
        <div class="col-md-6">
          <div v-for="(keyValue, i) in keyValues" :key="i" class="d-flex">
            <v-text-field
              v-model="keyValue.key"
              outlined
              dense
              style="width: 8rem"
              class="mr-4"
            />
            <v-text-field v-model="keyValue.value" outlined dense />
            <v-btn
              icon
              color="red"
              class="ml-2"
              @click="
                keyValues = keyValues.filter(
                  (kv) => keyValues.indexOf(kv) !== i
                )
              "
            >
              <v-icon> mdi-delete </v-icon>
            </v-btn>
          </div>
          <v-btn
            color="secondary darken-1"
            class="mb-4 py-6"
            elevation="0"
            @click="
              keyValues.push({
                key: '',
                value: '',
              })
            "
          >
            <v-icon color="grey darken-3" left> mdi-plus </v-icon>
            <span class="grey--text text--darken-3">Add field</span>
          </v-btn>
          <v-btn
            elevation="0"
            :disabled="!canSave"
            color="primary"
            class="py-6 w-100"
            @click="saveChanges()"
          >
            Save changes
          </v-btn>
        </div>
      </div>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "BusinessCard",
  data() {
    return {
      businessCard: null,
      keyValues: null,
      isTtsLoading: false,
      audio: null,
    };
  },
  created() {
    this.getCard();
  },
  computed: {
    canSave() {
      return (
        this.keyValues.filter(
          (kv) => kv.key.trim().length === 0 || kv.value.trim().length === 0
        ).length === 0
      );
    },
    id(){
      return this.$route.params.id;
    }
  },
  watch:{
    id(){
      this.getCard();
    }
  },
  methods: {
    getCard() {
      const { id } = this.$route.params;
      this.$http.get(`/business-card/${id}`).then(({ data }) => {
        this.businessCard = data;
        this.keyValues = this.getKeyValue(this.businessCard.entities.S);
      });
    },
    getKeyValue(obj) {
      const keyValues = Object.keys(obj)
        .map((key) => ({
          key: key,
          value: obj[key],
        }))
        .map((keyValue) => ({
          key: keyValue.key,
          value: keyValue.value.reduce((acc, curr) => acc + curr + " ", ""),
        }));
      return keyValues;
    },
    readCard() {
      if (this.isTtsLoading) return;
      this.isTtsLoading = true;
      this.$http
        .post(`business-card/${this.$route.params.id}/tts`)
        .then(({ data }) => {
          this.audio?.pause();
          const { objectUrl } = data;
          this.audio = new Audio(objectUrl);
          this.audio.play();
        })
        .catch((err) => {
          alert(err);
        })
        .finally(() => {
          this.isTtsLoading = false;
        });
    },
    saveChanges() {
      const payload = {};
      this.keyValues.forEach((keyValue) => {
        payload[keyValue.key] = [keyValue.value];
      });
      this.$http
        .put(`business-card/${this.$route.params.id}`, { params: payload })
        .then(() => {
          alert("Changes saved.");
        })
        .catch(() => {
          alert("Something went wrong, please try again.");
        });
    },
    beforeRouteLeave(to, from, next) {
      this.audio?.pause();
      this.audio = null;
      next();
    },
  },
};
</script>