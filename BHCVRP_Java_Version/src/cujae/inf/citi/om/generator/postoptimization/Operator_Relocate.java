/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package cujae.inf.citi.om.generator.postoptimization;

import cujae.inf.citi.om.generator.solution.Route;
import java.util.ArrayList;

/**
 *
 * @author nanda
 */
public class Operator_Relocate {
    
    public void toOptimize(Route route) {
        ArrayList<Integer> listOpt = new ArrayList<>(route.getListIdCustomers());
        double bestCost = route.getCostSingleRoute();
        double currentCost = 0.0;

        for (int i = 0; i < listOpt.size(); i++) {
            for (int j = i + 1; j < listOpt.size(); j++) {
                // Attempt to move the customer at position i to all other positions
                ArrayList<Integer> newRoute = new ArrayList<>(listOpt);
                int temp = newRoute.get(i);
                newRoute.set(i, newRoute.get(j));
                newRoute.set(j, temp);

                double newCost = calculateTotalDistance(newRoute);
                if (newCost < bestCost) {
                    bestCost = newCost;
                    listOpt = newRoute;
                }
            }
        }

        route.setListIdCustomers(listOpt);
        route.setCostRoute(bestCost);
    }

    private double calculateTotalDistance(ArrayList<Integer> newRoute) {
        throw new UnsupportedOperationException("Not supported yet."); // Generated from nbfs://nbhost/SystemFileSystem/Templates/Classes/Code/GeneratedMethodBody
    }

    
}
