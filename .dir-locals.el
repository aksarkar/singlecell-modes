((org-mode . ((org-publish-project-alist .
          (("singlecell-modes-org" . (:base-directory "/project2/mstephens/aksarkar/projects/singlecell-modes/org"
                                              :publishing-directory "/project2/mstephens/aksarkar/projects/singlecell-modes/docs"
                                              :publishing-function org-html-publish-to-html
                                              :exclude "setup.org"
                                              :sitemap-title "Single cell analysis of singlecell-modesune cases"
                                              :htmlized-source t
                                              ))
            ("singlecell-modes-fig" . (:base-directory "/project2/mstephens/aksarkar/projects/singlecell-modes/org"
                                              :publishing-directory "/project2/mstephens/aksarkar/projects/singlecell-modes/docs"
                                              :publishing-function org-publish-attachment
                                              :base-extension "png\\|\\|svg"
                                              :recursive t
                                              ))
            ("singlecell-modes" . (:components ("singlecell-modes-org" "singlecell-modes-fig"))))))))
