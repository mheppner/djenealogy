'use strict';

(function(angular) {
    
    angular.module('djenealogy.controllers.people', [])
    
        .controller('PeopleCtrl', [
            '$scope',
            '$state',
            '$http',
            'ngTableParams',
            'IndividualSrvc',
            function($scope,
                    $state,
                    $http,
                    ngTableParams,
                    IndividualSrvc) {
                
                $scope.tableParams = new ngTableParams({
                    page: parseInt($scope.$storage.individuals_page) || 1,
                    count: parseInt($scope.$storage.individuals_count) || 10,
                    sorting: {
                        surname: 'asc',
                    },
                    filter: {
                        surname: $scope.$storage.individuals_search || ''
                    }
                }, {
                    total: 0,
                    getData: function($defer, params) {
                        $scope.$storage.individuals_page = params.page();
                        $scope.$storage.individuals_count = params.count();
                        
                        var opts = {
                            'page': params.page(),
                            'page_size': params.count(),
                        };
                        
                        var filters = params.filter();
                        if ('surname' in filters) {
                            opts['search'] = filters['surname'];
                            $scope.$storage.individuals_search= filters['surname'];
                        }
                        
                        var sorting = params.sorting();
                        if ('surname' in sorting) {
                            opts['ordering'] = (sorting['surname'] == 'asc' ? 'surname' : '-surname');
                        } else if ('given_name' in sorting) {
                            opts['ordering'] = (sorting['given_name'] == 'asc' ? 'given_name' : '-given_name');
                        }
                        
                        
                        IndividualSrvc.get(opts).$promise.then(function(data) {
                            params.total(data.count);
                            $defer.resolve(data.results);
                        }, function(data) {
                            
                        });
                    }
                });
                
                
            }
        ])
        
        .controller('IndividualCtrl', [
            '$scope',
            '$state',
            'individual',
            '$filter',
            function($scope,
                     $state,
                     individual,
                     $filter) {
                
                $scope.individual = individual;
                
                // find birth and death events
                var birth = $filter('filter')(individual.events, {type: 'BIRT'}),
                    death = $filter('filter')(individual.events, {type: 'DEAT'});
                   
                // attach first birth and death to scope 
                if (birth.length) {
                    $scope.individual.birth = birth[0];
                }
                if (death.length) {
                    $scope.individual.death = death[0];
                }
                
            }
        
        ])
    
        ;
    
})(angular);
