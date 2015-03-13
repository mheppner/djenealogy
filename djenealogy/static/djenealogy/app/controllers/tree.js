'use strict';

(function(angular) {
    
    angular.module('djenealogy.controllers.tree', [])
    
        .controller('TreeCtrl', [
            '$scope',
            '$state',
            'tree',
            '$window',
            '$timeout',
            '$modal',
            function($scope,
                    $state,
                    tree,
                    $window,
                    $timeout,
                    $modal) {
                
                $scope.indv_tree = tree.data;
                
                // set default view models
                $scope.$storage.tree_width = $scope.$storage.tree_width || 'container';
                $scope.$storage.tree_zoom = $scope.$storage.tree_zoom || 1;
                
                $scope.zoom = function(delta) {
                    $scope.$storage.tree_zoom += delta;
                };
                
                $scope.center = function() {
                    $scope.$emit('pedigreeTreeCenter');
                };
                
                $scope.$watch('$storage.tree_zoom', function(newVal, oldVal) {
                    $scope.$emit('pedigreeTreeAdjust');
                });
                
                $scope.$watch('$storage.tree_width', function(newVal, oldVal) {
                    $scope.$emit('pedigreeTreeAdjust');
                });
                
                $scope.$on('pedigreeTreeIndividualClick', function(e, indv) {
                    $modal.open({
                        templateUrl: $scope.APP_URL + 'templates/tree/modal.html',
                        backdrop: true,
                        controller: 'TreeIndividualModalCtrl',
                        resolve: {
                            individual: ['IndividualSrvc', function(IndividualSrvc) {
                                return IndividualSrvc.get({id: indv.id}).$promise;
                            }]
                        }
                    }).result.then(function() {
                        
                    }, function() {
                        
                    });
                });
                
            }
        ])
        
        .controller('TreeIndividualModalCtrl', [
            '$scope',
            '$modalInstance',
            'individual',
            '$filter',
            function($scope,
                     $modalInstance,
                     individual,
                     $filter) {
             
                $scope.i = individual;
                
                // find birth and death events
                var birth = $filter('filter')(individual.events, {type: 'BIRT'}),
                    death = $filter('filter')(individual.events, {type: 'DEAT'});
                   
                // attach first birth and death to scope 
                if (birth.length) {
                    $scope.i.birth = birth[0];
                }
                if (death.length) {
                    $scope.i.death = death[0];
                }
                
                $scope.close = function() {
                    $modalInstance.close();
                };
            
            }
        ])
        
        ;
    
})(angular);
