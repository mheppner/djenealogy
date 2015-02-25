'use strict';

(function(angular) {
    
    angular.module('djenealogy.controllers.families', [])
    
        .controller('FamiliesCtrl', [
            '$scope',
            '$state',
            '$http',
            'ngTableParams',
            'FamilySrvc',
            function($scope,
                    $state,
                    $http,
                    ngTableParams,
                    FamilySrvc) {
                
                $scope.tableParams = new ngTableParams({
                    page: parseInt($scope.$storage.families_page) || 1,
                    count: parseInt($scope.$storage.families_count) || 10,
                    sorting: {
                        husband__surname: 'asc',
                    },
                    filter: {
                        surname: $scope.$storage.families_search || ''
                    }
                }, {
                    total: 0,
                    getData: function($defer, params) {
                        $scope.$storage.families_page = params.page();
                        $scope.$storage.families_count = params.count();
                        
                        var opts = {
                            'page': params.page(),
                            'page_size': params.count(),
                        };
                        
                        var filters = params.filter();
                        if ('surname' in filters) {
                            opts['search'] = filters['surname'];
                            $scope.$storage.families_search = filters['surname'];
                        }
                        
                        var sorting = params.sorting();
                        if ('husband__surname' in sorting) {
                            opts['ordering'] = (sorting['husband__surname'] == 'asc' ? 'husband__surname' : '-husband__surname');
                        } else if ('husband__given_name' in sorting) {
                            opts['ordering'] = (sorting['husband__given_name'] == 'asc' ? 'husband__given_name' : '-husband__given_name');
                        } else if ('wife__surname' in sorting) {
                            opts['ordering'] = (sorting['wife__surname'] == 'asc' ? 'wife__surname' : '-wife__surname');
                        } else if ('wife__given_name' in sorting) {
                            opts['ordering'] = (sorting['wife__given_name'] == 'asc' ? 'wife__given_name' : '-wife__given_name');
                        }
                        
                        
                        FamilySrvc.get(opts).$promise.then(function(data) {
                            params.total(data.count);
                            $defer.resolve(data.results);
                        }, function(data) {
                            
                        });
                    }
                });
                
                
            }
        ])
        
        .controller('FamilyCtrl', [
            '$scope',
            '$state',
            'family',
            function($scope,
                     $state,
                     family) {
                
                $scope.family = family;
            }
        
        ])
    
        ;
    
})(angular);
