/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package cujae.inf.citi.om.generator.postoptimization;

import cujae.inf.citi.om.solution.Route;
import java.util.ArrayList;
import java.util.Collections;

/**
 *
 * @author nanda
 */
public class Operator_2opt {
    
    public void toOptimize(Route route) {
        ArrayList<Integer> listOpt = new ArrayList<>(route.getListIdCustomers());
        double bestCost = route.getCostSingleRoute();
        double currentCost = 0.0;

        for (int i = 1; i < listOpt.size() - 1; i++) {
            for (int j = i + 1; j < listOpt.size(); j++) {
                if (i < j) {
                    ArrayList<Integer> newRoute = new ArrayList<>(listOpt);
                    Collections.reverse(newRoute.subList(i, j));

                    double newCost = calculateTotalDistance(newRoute);
                    if (newCost < bestCost) {
                        bestCost = newCost;
                        listOpt = newRoute;
                    }
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
