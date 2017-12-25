/**
 * VirtualMachinesController
 *
 * @description :: Server-side logic for managing virtualmachines
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

const request = require('request'),
      sleep = require('system-sleep');

module.exports = {

  create: function(req, res, next) {
    VirtualMachines.create(req.params.all(), function virtualMachineCreated(err, virtualMachine) {
      if (err) return next(err);

      console.log(virtualMachine);

      var options = {
        url: 'http://145.28.154.147:8000',
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        json: {Action: "Create", virtualMachine: virtualMachine}
      };

      sleep(3000);

      request(options, function(err, res, body) {
        if (err) return;

        if (body) {
          virtualMachine.ip = JSON.stringify(body.IP);
          virtualMachine.status = JSON.stringify(body.State);

          console.log(body);

        }
      });
      sleep(6000);

      VirtualMachines.update(virtualMachine.id, virtualMachine, function virtualMachineUpdated (err) {
        if (err) {
          return next(err);
        }

        res.redirect('/user/virtualPanel/'+ req.session.User.id);
      });
    });
  },

  destroy: function(req, res, next) {
    VirtualMachines.findOne(req.param('id'), function foundVirtualMachine(err, virtualMachine){
      if (err) return next(err);

      if (!virtualMachine) return next('VirtualMachine doesn\'t exist.');

      var options = {
        url: 'http://145.28.154.147:8000',
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        json: {Action: "Remove", virtualMachine: virtualMachine}
      };

      sleep(3000);

      request(options, function(err, res, body) {
        if (err) return;

        if (body) {
          virtualMachine.ip = JSON.stringify(body.IP);
          virtualMachine.status = JSON.stringify(body.State);

          console.log(body);

        }
      });
      sleep(6000);

      VirtualMachines.destroy(req.param('id'), function virtualMachineDestroyed (err){
        if (err) return next(err);

        res.redirect('/user/virtualPanel/'+ req.session.User.id);
      });
    });
  },

  start: function(req, res, next) {
    VirtualMachines.findOne(req.param('id'), function foundVirtualMachine(err, virtualMachine) {
      if (err) return next(err);
      if (!virtualMachine) return next(err);

      var options = {
        url: 'http://145.28.154.147:8000',
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        json: {Action: "Start", virtualMachine: virtualMachine}
      };

      sleep(3000);

      request(options, function(err, res, body) {
        if (err) return;

        if (body) {

          console.log(body);

          virtualMachine.ip = JSON.stringify(body.IP);
          virtualMachine.status = JSON.stringify(body.State);

        }
      });
      sleep(6000);

      VirtualMachines.update(virtualMachine.id, virtualMachine, function virtualMachineUpdated (err) {
        if (err) {
          return next(err);
        }

        res.redirect('/user/virtualPanel/'+ req.session.User.id);
      });
    });
  },

  stop: function(req, res, next) {
    VirtualMachines.findOne(req.param('id'), function foundVirtualMachine(err, virtualMachine) {
      if (err) return next(err);
      if (!virtualMachine) return next(err);

      var options = {
        url: 'http://145.28.154.147:8000',
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        json: {Action: "Suspend", virtualMachine: virtualMachine}
      };

      sleep(3000);

      request(options, function(err, res, body) {
        if (err) return;

        if (body) {
          virtualMachine.ip = JSON.stringify(body.IP);
          virtualMachine.status = JSON.stringify(body.State);

          console.log(body);
        }
      });
      sleep(6000);

      VirtualMachines.update(virtualMachine.id, virtualMachine, function virtualMachineUpdated (err) {
        if (err) {
          return next(err);
        }

        res.redirect('/user/virtualPanel/'+ req.session.User.id);
      });
    });
  }
};

