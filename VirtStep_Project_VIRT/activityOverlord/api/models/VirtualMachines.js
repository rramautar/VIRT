/**
 * VirtualMachines.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/documentation/concepts/models-and-orm/models
 */

module.exports = {

  attributes: {
    name: {
      type: 'string',
      required: 'true'
    },

    description: {
      type: 'mediumtext'
    },

    setup: {
      type: 'integer',
      required: 'true'
    },

    os: {
      type: 'integer',
      required: 'true'
    },

    ip: {
      type: 'string',
      defaultsTo: 'not yet configured'
    },

    status: {
      type: 'string',
      defaultsTo: 'not yet configured'
    },

    owner: {
      model: 'user',
      required: 'true'
    }
  }
};

