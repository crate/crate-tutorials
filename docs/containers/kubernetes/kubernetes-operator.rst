.. _cratedb-kubernetes-operator:

====================================
Run CrateDB with Kubernetes Operator
====================================

The `CrateDB Kubernetes Operator`_ provides a convenient way to run `CrateDB`_
clusters inside Kubernetes.


Installation
============

`Helm`_ must be installed to install the Crate operator chart.
Once Helm is set up properly, add the repo as follows:

.. code-block:: console

    helm repo add crate-operator https://crate.github.io/crate-operator

Install the crate-operator chart:

.. code-block:: console

    helm install crate-operator crate-operator/crate-operator

.. NOTE::

    To be able to deploy the custom resource ``CrateDB`` to a Kubernetes cluster,
    the API needs to be extended with a `Custom Resource Definition`_ (CRD).
    It is installed as a dependency of the ``crate-operator`` chart, but it can be
    installed separately. See the `Crate Operator Chart documentation`_ for
    further details.

Run CrateDB
===========

A minimal custom resource for a three-node CrateDB cluster may look like this:

``dev-cluster.yaml``:

.. code-block:: yaml

   apiVersion: cloud.crate.io/v1
   kind: CrateDB
   metadata:
     name: my-cluster
     namespace: dev
   spec:
     cluster:
       imageRegistry: crate
       name: crate-dev
       version: 4.3.1
     nodes:
       data:
       - name: default
         replicas: 3
         resources:
           limits:
             cpu: 4
             memory: 4Gi
           disk:
             count: 1
             size: 128GiB
             storageClass: default
           heapRatio: 0.5

.. code-block:: console

   $ kubectl --namespace dev create -f dev-cluster.yaml
   ...

   $ kubectl --namespace dev get cratedbs
   NAMESPACE   NAME         AGE
   dev         my-cluster   36s

.. NOTE::

    You can find the Crate Operator features in the ``Features`` section
    of `CrateDB Kubernetes Operator`_.


.. _CrateDB Kubernetes Operator: https://github.com/crate/crate-operator
.. _CrateDB: https://github.com/crate/crate
.. _Helm: https://helm.sh
.. _Custom Resource Definition: https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/
.. _Crate Operator Chart documentation: https://github.com/crate/crate-operator/blob/master/deploy/charts/crate-operator/README.md
