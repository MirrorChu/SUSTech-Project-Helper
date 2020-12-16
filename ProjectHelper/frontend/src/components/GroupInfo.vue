<template>
  <div>
  <h2>Group Info</h2>
    Group Introduction: {{ this.$props.groupInfo.group_introduction }}
    <br>
    Group Name: {{ this.$props.groupInfo.group_name }}
    <br>
    Captain Name: {{ this.$props.groupInfo.captain_name }}
    <br>
    Members: {{ this.$props.membersList }}
    <br>
    <el-divider></el-divider>
    <h2>Wanna invite someone?</h2>
    <el-select v-model="toInviteList" multiple clearable placeholder="select people to invite">
      <el-option
        v-for="item in invitableList"
        :key="item.value"
        :label="item.label"
        :value="item.value">
      </el-option>
    </el-select>
    <el-button @click="onClickInvite">invite</el-button>
    <el-divider></el-divider>
  </div>
</template>

<script>
export default {
  props: {
    groupInfo: {
      required: true
    },
    membersList: {
      required: true
    },
    sid: {
      type: String,
      required: true
    },
    pswd: {
      type: String,
      requires: true
    }
  },
  created() {

  },
  data() {
    return {
      toInviteList: [],
      invitableList: [
        {value: '11810201', label: '11810201'},
        {value: '11810202', label: '11810202'},
        {value: '11810203', label: '11810203'}
      ],
    }
  },
  methods: {
    onClickInvite() {
      if (this.toInviteList.length === 0) {
        alert('You are not inviting anyone!')
      } else {
        alert(this.toInviteList)
      }
    },
    onFocusPerson(item) {
      alert(item)
    }
  },
  name: "GroupInfo"
}
</script>

<style scoped>

</style>
