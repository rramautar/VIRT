/**
 * CodeTableController
 *
 * @description :: Server-side logic for managing codetables
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

module.exports = {

  index: function (req, res, next) {
    CodeTable.find(function foundOptions (err, options){
      if (err) return next(err);

      res.view({
        options: options
      });
    });
  },

  create: function (req, res, next) {

    codetable.create( req.params.all(), function(err){

      if (err) {
        console.log(err);
        req.session.flash = {
          err: err
        };

        return res.redirect('/codeTable');
      }

      codetable.save(function(err){
        if (err) return next(err);

        res.redirect('/codeTable');
      });
    });
  }

};

