/**
 * User.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/documentation/concepts/models-and-orm/models
 */

module.exports = {

  schema: true,

  attributes: {

    name: {
      type: 'string',
      required: true
    },

    title: {
      type: 'string'
    },

    email: {
      type: 'string',
      email: true,
      required: true,
      unique: true
    },

    online: {
      type: 'boolean',
      defaultsTo: false
    },

    admin: {
      type: 'boolean',
      defaultsTo: false
    },

    encryptedPassword: {
      type: 'string'
    },

    virtualMachines: {
      collection: 'virtualmachines',
      via: 'owner'
    },

    toJSON: function() {
        var obj = this.toObject();
        delete obj.password;
        delete obj.confirmation;
        delete obj.encryptedPassword;
        delete obj._csrf;
        return obj;
    }

  },

  beforeValidate: function (values, next) {
    console.log(values)
    if (typeof values.admin !== 'undefined') {
      if (values.admin === 'unchecked') {
        values.admin = false;
      } else if (values.admin[1] === 'on') {
        values.admin = true;
      }
    }
    next();
  },

  beforeCreate: function (values, next) {

    if (!values.password || values.password != values.confirmation) {
      return next({err: ["Password doesn't match password confirmation: "+ values.password +" & "+ values.confirmation+ " "]});
    }

    require('bcrypt').hash(values.password, 10, function passwordEncrypted(err, encryptedPassword){
      if (err) return next(err);
      values.encryptedPassword = encryptedPassword;
      //values.online= true;
      next();
    });
  }
};

