/**
 * CodeTable.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/documentation/concepts/models-and-orm/models
 */

module.exports = {

  attributes: {

    name: {
      type: 'string',
      required: true
    },

    description: {
      type: 'string'
    },

    ram: {
      type: 'string',
      required: true
    },

    rom: {
      type: 'string',
      required: true
    },

    cpu: {
      type: 'string',
      required: true
    },

    option: {
      model: 'virtualMachines',
      required: true
    }

  }
};

