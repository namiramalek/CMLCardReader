<template>
  <div>
    <div class="row">
      <div
        v-for="businessCard in businessCards"
        :key="businessCard.id.S"
        class="col-12 b-4"
      >
        <div class="pa-4 blue-grey lighten-5">
          <div class="row">
            <div class="col-md-6">
              <router-link :to="`business-card/${businessCard.id.S}`">
                <div
                  class="business-card-photo"
                  :style="`background-image: url(${businessCard.s3_url.S})`"
                ></div>
              </router-link>
            </div>
            <div class="col-md-6">
              <router-link :to="`business-card/${businessCard.id.S}`">
                <p
                  v-for="(entity, i) in getEntries(businessCard.entities.S)"
                  :key="i"
                >
                  <span
                    class="
                      text-capitalize
                      font-weight-medium
                      grey--text
                      text--darken-3
                    "
                    >{{ entity[0] }}:</span
                  >
                  <span class="font-weight-bold">
                    {{ entity[1].reduce((acc, cur) => acc + cur + " ", "") }}
                  </span>
                  &nbsp;
                  <span class="font-weight-bold">{{ entity.value }}</span>
                </p>
              </router-link>
              <div>
                <v-btn
                  :to="`business-card/${businessCard.id.S}`"
                  elevation="0"
                  color="primary"
                  class="mr-4"
                >
                  Edit
                </v-btn>
                <v-btn
                  @click="deleteItem(businessCard.id.S)"
                  color="error"
                  elevation="0"
                  outlined
                >
                  Delete
                </v-btn>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "BusinessCardTable",
  props: {
    businessCards: Array,
  },
  methods: {
    getEntries(obj) {
      return Object.entries(obj);
    },
    editBusinessCard(i) {
      console.log(i);
    },
    deleteItem(id) {
      const isConfirmed = confirm("Are you sure?");
      if (!isConfirmed) return;
      return this.$emit("delete", id);
    },
  },
};
</script>

<style lang="stylus" scoped>
.business-card-photo {
  aspect-ratio: 3 / 2;
  width: 100%;
  max-width: 100%;
  background-position: center;
  background-size: cover;
}
</style>