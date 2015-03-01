'use strict';

(function(angular) {
    
    angular.module('djenealogy.controllers.tree', [])
    
        .controller('TreeCtrl', [
            '$scope',
            '$state',
            'tree',
            
            function($scope,
                    $state,
                    tree) {
                
                $scope.tree = tree.data;
                
                // set default view models
                $scope.$storage.tree_width = $scope.$storage.tree_width || 'container';
                $scope.$storage.tree_zoom = $scope.$storage.tree_zoom || 1;
                
                $scope.zoom = function(delta) {
                    $scope.$storage.tree_zoom += delta;
                };
                
            }
        ])
        
        ;
    
})(angular);
