'use strict';
(function(angular) {
    angular.module('djenealogy.services', [])

        .factory('IndividualSrvc', ['URLS', '$resource',
            function(URLS, $resource) {
                return $resource(URLS.api.individuals + ':id/', {}, {
                    update: { method: 'PUT' },
                    options:  { method: 'OPTIONS', cache: true }
                });
            }
        ])
        
        .factory('FamilySrvc', ['URLS', '$resource',
            function(URLS, $resource) {
                return $resource(URLS.api.families + ':id/', {}, {
                    update: { method: 'PUT' },
                    options:  { method: 'OPTIONS', cache: true }
                });
            }
        ])
        
      
        ;
})(angular);